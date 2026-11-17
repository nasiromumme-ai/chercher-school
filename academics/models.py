from django.db import models

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
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=50)
    parent_phone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='students/', blank=True, null=True)

    def __str__(self):
        return self.name

# --- NEW MODEL ADDED BELOW ---

class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    exam_date = models.DateField()

    def __str__(self):
        return f"{self.student.name} - {self.subject}"