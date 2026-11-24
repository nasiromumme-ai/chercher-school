from django.contrib import admin
from .models import MonthlyReport


@admin.register(MonthlyReport)
class MonthlyReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'month', 'year', 'grade', 'allow_download', 'uploaded_at')
    list_editable = ('allow_download',)
    list_filter = ('allow_download', 'year', 'month', 'grade')
    search_fields = ('title', 'grade')