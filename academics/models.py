from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
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