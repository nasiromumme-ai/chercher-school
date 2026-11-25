import datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from registration.models import RegisteredStudent


class Subject(models.Model):
    GRADE_CHOICES = [
        ('9', 'Grade 9'),
        ('10', 'Grade 10'),
        ('11', 'Grade 11'),
        ('12', 'Grade 12'),
    ]
    STREAM_CHOICES = [
        ('Common', 'Common'),
        ('Natural', 'Natural Science'),
        ('Social', 'Social Science'),
    ]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True, null=True)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    stream = models.CharField(max_length=15, choices=STREAM_CHOICES, default='Common')

    class Meta:
        ordering = ['grade', 'stream', 'name']
        unique_together = ('name', 'grade', 'stream')

    def __str__(self):
        if self.grade in ['11', '12']:
            return f"{self.name} (Grade {self.grade} - {self.get_stream_display()})"
        return f"{self.name} (Grade {self.grade})"


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, help_text="e.g., Science, Languages, Humanities")
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to='teachers/', blank=True, null=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    STREAM_CHOICES = [
        ('Common', 'Common (Grade 9-10)'),
        ('Natural', 'Natural Science (Grade 11-12)'),
        ('Social', 'Social Science (Grade 11-12)'),
    ]

    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=50, help_text="e.g., 9, 10, 11, 12 or 9A")
    section = models.CharField(max_length=10, blank=True, help_text="e.g., A, B, C")
    stream = models.CharField(max_length=15, choices=STREAM_CHOICES, default='Common', blank=True)
    subjects = models.ManyToManyField(Subject, related_name='students', blank=True)
    parent_phone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='students/', blank=True, null=True)

    @property
    def grade_number(self):
        return ''.join(ch for ch in str(self.grade) if ch.isdigit())

    @property
    def parsed_section(self):
        if self.section:
            return self.section.strip().upper()
        letters = ''.join(ch for ch in str(self.grade) if ch.isalpha())
        return letters.upper()

    @property
    def class_label(self):
        g = self.grade_number or self.grade
        s = self.parsed_section
        return f"{g}{s}" if s else str(g)

    def save(self, *args, **kwargs):
        # Auto-extract section if someone types "9A" or "10B" into `grade`
        if not self.section and self.grade:
            letters = ''.join(ch for ch in str(self.grade) if ch.isalpha())
            if letters:
                self.section = letters.upper()
        elif self.section:
            self.section = self.section.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.class_label})"


@receiver(post_save, sender=Student)
def auto_assign_subjects_to_student(sender, instance, created, **kwargs):
    """Assigns existing matching subjects to Student.subjects without creating Subject rows."""
    grade_num = instance.grade_number
    if grade_num not in ['9', '10', '11', '12']:
        instance.subjects.clear()
        return

    if grade_num in ['9', '10']:
        matched_subjects = Subject.objects.filter(grade=grade_num, stream='Common')
    else:
        stream_val = instance.stream if instance.stream in ['Natural', 'Social'] else 'Common'
        matched_subjects = Subject.objects.filter(
            grade=grade_num,
            stream__in=[stream_val, 'Common']
        )

    # Read-only lookup + M2M assignment only; never creates Subject records
    instance.subjects.set(matched_subjects)


class StudentResult(models.Model):
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
    ]

    student = models.ForeignKey(RegisteredStudent, on_delete=models.CASCADE, related_name='results')
    subject_ref = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='results',
        verbose_name="Subject (Grade 9-12)"
    )
    subject = models.CharField(max_length=100, blank=True)
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES, default=1)
    section = models.CharField(max_length=10, blank=True, help_text="e.g., A, B, C (for class rank like 9A, 10B)")
    academic_year = models.CharField(max_length=20, default="2018", blank=True)
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    exam_date = models.DateField(default=datetime.date.today, blank=True)

    class Meta:
        ordering = ['student', 'semester', 'subject']

    @property
    def grade_number(self):
        if self.subject_ref and self.subject_ref.grade:
            return self.subject_ref.grade
        raw_grade = getattr(self.student, 'grade', '') or getattr(self.student, 'grade_level', '')
        return ''.join(ch for ch in str(raw_grade) if ch.isdigit())

    @property
    def resolved_section(self):
        if self.section:
            return self.section.strip().upper()
        reg_sec = getattr(self.student, 'section', '')
        if reg_sec:
            return str(reg_sec).strip().upper()
        raw_grade = getattr(self.student, 'grade', '') or ''
        letters = ''.join(ch for ch in str(raw_grade) if ch.isalpha())
        return letters.upper()

    @property
    def class_label(self):
        g = self.grade_number
        s = self.resolved_section
        return f"{g}{s}" if (g and s) else (g or "Unassigned")

    def save(self, *args, **kwargs):
        # Keep legacy `subject` char field synced when `subject_ref` is chosen
        if self.subject_ref:
            self.subject = self.subject_ref.name
        if self.section:
            self.section = self.section.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        subject_label = self.subject_ref.name if self.subject_ref else self.subject
        return f"{self.student.first_name} {self.student.last_name} - {subject_label} (Sem {self.semester})"