from django.db import models

class Alumni(models.Model):
    name = models.CharField(max_length=100)
    graduation_year = models.CharField(max_length=10, help_text="e.g., 2020")
    current_role = models.CharField(max_length=200, help_text="e.g., Medical Student, Software Engineer")
    institution = models.CharField(max_length=200, help_text="e.g., Addis Ababa University, Google")
    photo = models.ImageField(upload_to='alumni/', blank=True, null=True)
    message = models.TextField(blank=True, help_text="A short message or advice for current students")

    class Meta:
        ordering = ['-graduation_year']
        verbose_name_plural = "Alumni"

    def __str__(self):
        return f"{self.name} ({self.graduation_year})"