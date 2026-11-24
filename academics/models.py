from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    grade = models.CharField(max_length=50)
    stream = models.CharField(max_length=15, choices=STREAM_CHOICES, default='Common', blank=True)
    subjects = models.ManyToManyField(Subject, related_name='students', blank=True)
    parent_phone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='students/', blank=True, null=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Student)
def auto_assign_subjects_to_student(sender, instance, created, **kwargs):
    """Assigns existing matching subjects to Student.subjects without creating Subject rows."""
    grade_num = ''.join(ch for ch in str(instance.grade) if ch.isdigit())
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
    score = models.DecimalField(max_digits=5, decimal_places=2)
    exam_date = models.DateField()

    def save(self, *args, **kwargs):
        # Keep legacy `subject` char field synced when `subject_ref` is chosen
        if self.subject_ref:
            self.subject = self.subject_ref.name
        super().save(*args, **kwargs)

    def __str__(self):
        subject_label = self.subject_ref.name if self.subject_ref else self.subject
        return f"{self.student.first_name} {self.student.last_name} - {subject_label}"