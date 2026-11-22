from django.db import models

class RegisteredStudent(models.Model):
    # Choices for dropdowns
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    GRADE_CHOICES = [('9', 'Grade 9'), ('10', 'Grade 10'), ('11', 'Grade 11'), ('12', 'Grade 12')]
    PROGRAM_CHOICES = [('Regular', 'Regular'), ('Night', 'Night'), ('Weekend', 'Weekend')]

    # Personal Info
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50, unique=True, help_text="e.g., CSS-2026-001")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    previous_school = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='registered_students/', blank=True, null=True)

    # Academic Info
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    program = models.CharField(max_length=20, choices=PROGRAM_CHOICES)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    class Meta:
        ordering = ['-registered_at']
        verbose_name_plural = "Registered Students"