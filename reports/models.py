from django.db import models


class MonthlyReport(models.Model):
    MONTHS = [
        ('January', 'January'), ('February', 'February'), ('March', 'March'),
        ('April', 'April'), ('May', 'May'), ('June', 'June'),
        ('July', 'July'), ('August', 'August'), ('September', 'September'),
        ('October', 'October'), ('November', 'November'), ('December', 'December')
    ]

    title = models.CharField(max_length=200, help_text="e.g., Grade 9 Term 1 Report")
    month = models.CharField(max_length=20, choices=MONTHS)
    year = models.CharField(max_length=4, help_text="e.g., 2026")
    grade = models.CharField(max_length=50, blank=True, help_text="e.g., Grade 9 (leave blank for all)")
    file = models.FileField(upload_to='reports/', help_text="Upload PDF or Excel file")
    allow_download = models.BooleanField(
        default=False,
        help_text="Allow public visitors to download this report. Leave unchecked for view-only access."
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', '-month']
        verbose_name_plural = "Monthly Reports"

    def __str__(self):
        return f"{self.month} {self.year} - {self.title}"