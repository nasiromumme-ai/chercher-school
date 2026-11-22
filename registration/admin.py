from django.contrib import admin
from .models import RegisteredStudent

@admin.register(RegisteredStudent)
class RegisteredStudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'grade', 'program', 'phone_number')
    list_filter = ('grade', 'program', 'gender')
    search_fields = ('first_name', 'last_name', 'student_id')