from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "News"

    def __str__(self):
        return self.title


class Gallery(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        return self.title


# --- NEW MODELS ADDED BELOW ---

class TopStudent(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=10, help_text="e.g., 2023, 2024")
    score = models.CharField(max_length=50, help_text="e.g., 595/600 or GPA 4.0")
    grade = models.CharField(max_length=50, blank=True, help_text="e.g., Grade 12 Natural Science")
    photo = models.ImageField(upload_to='top_students/', blank=True, null=True)

    class Meta:
        ordering = ['-year', 'name']
        verbose_name_plural = "Top Students"

    def __str__(self):
        return f"{self.name} ({self.year})"


class SchoolStructure(models.Model):
    role = models.CharField(max_length=100, help_text="e.g., Director, Vice Director")
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='structure/', blank=True, null=True)
    message = models.TextField(blank=True, help_text="Message from the Director or role description")

    class Meta:
        verbose_name_plural = "School Structure & Director"

    def __str__(self):
        return f"{self.role} - {self.name}"


# --- CONTACT FORM MODEL ---

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Contact Messages"
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.subject} - {self.name}"


# --- NEW EVENT MODEL ---

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.CharField(max_length=100, blank=True, help_text="e.g., 9:00 AM - 12:00 PM")
    location = models.CharField(max_length=200, blank=True, help_text="e.g., Main Hall")

    class Meta:
        ordering = ['date']
        verbose_name_plural = "Events"

    def __str__(self):
        return f"{self.title} - {self.date}"


# --- NEW SUBSCRIBER MODEL ---

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


# --- MEETINGS, DECISIONS & STUDENT COOPERATION MODEL ---

class SchoolHighlight(models.Model):
    CATEGORY_CHOICES = [
        ('weekly_meeting', 'Weekly Meeting Photo'),
        ('monthly_meeting', 'Monthly Meeting Photo'),
        ('staff_decision', 'Staff Meeting Decision'),
        ('student_cooperation', 'Teacher & Student Cooperation'),
    ]

    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    summary = models.TextField(help_text="Meeting decisions, key notes, or cooperation highlights.")
    photo = models.ImageField(upload_to='highlights/', blank=True, null=True)
    date_recorded = models.DateField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_recorded', '-id']
        verbose_name_plural = "School Highlights"

    def __str__(self):
        return f"{self.get_category_display()} - {self.title}"