from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'grade_applying', 'parent_name', 'phone', 'status', 'applied_at')
    list_filter = ('status', 'grade_applying')
    search_fields = ('student_name', 'parent_name', 'phone')