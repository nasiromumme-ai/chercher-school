from django.db import models

class Application(models.Model):
    student_name = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    previous_school = models.CharField(max_length=200)
    grade_applying = models.CharField(max_length=50, help_text="e.g., Grade 9")
    message = models.TextField(blank=True, help_text="Any additional information")
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending', choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')])

    def __str__(self):
        return f"{self.student_name} - {self.grade_applying} ({self.status})"