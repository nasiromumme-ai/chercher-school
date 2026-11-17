from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Teacher, Student, StudentResult

# Setup for Students
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('name', 'grade', 'parent_phone')
        import_id_fields = ('name',)

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = ('name', 'grade', 'parent_phone')
    search_fields = ('name', 'grade')
    list_filter = ('grade',)

# Setup for Teachers
class TeacherResource(resources.ModelResource):
    class Meta:
        model = Teacher
        fields = ('name', 'subject', 'department', 'phone', 'email')

@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    resource_class = TeacherResource
    list_display = ('name', 'subject', 'department', 'phone')
    search_fields = ('name', 'subject', 'department')
    list_filter = ('department',)

# --- NEW RESULT ADMIN ADDED BELOW ---

@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'score', 'exam_date')
    list_filter = ('subject', 'exam_date')
    search_fields = ('student__name', 'subject')