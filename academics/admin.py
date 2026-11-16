from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Teacher, Student

# Setup for Students
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('name', 'grade', 'parent_phone') # Exclude 'id' and 'image' for easier upload
        import_id_fields = ('name',) # Use name as the unique identifier if needed, or leave default

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
        fields = ('name', 'subject', 'phone', 'email')

@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    resource_class = TeacherResource
    list_display = ('name', 'subject', 'phone')
    search_fields = ('name', 'subject')