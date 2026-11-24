from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Subject, Teacher, Student, StudentResult


# Setup for Subjects
class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject
        fields = ('id', 'name', 'code', 'grade', 'stream')
        import_id_fields = ('code',)


@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    resource_class = SubjectResource
    list_display = ('name', 'code', 'grade_badge', 'stream_badge')
    list_filter = ('grade', 'stream')
    search_fields = ('name', 'code')
    ordering = ('grade', 'stream', 'name')
    list_per_page = 50

    @admin.display(description='Grade', ordering='grade')
    def grade_badge(self, obj):
        colors = {
            '9': ('#e0f2fe', '#0369a1'),
            '10': ('#dcfce7', '#15803d'),
            '11': ('#fef3c7', '#b45309'),
            '12': ('#ede9fe', '#6d28d9'),
        }
        bg, fg = colors.get(str(obj.grade), ('#f1f5f9', '#334155'))
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:999px;font-weight:600;font-size:0.78rem;display:inline-block;">Grade {}</span>',
            bg, fg, obj.grade
        )

    @admin.display(description='Stream', ordering='stream')
    def stream_badge(self, obj):
        stream_styles = {
            'Common': ('#f1f5f9', '#334155', 'Common'),
            'Natural': ('#ccfbf1', '#0f766e', 'Natural Science'),
            'Social': ('#fae8ff', '#86198f', 'Social Science'),
        }
        bg, fg, label = stream_styles.get(obj.stream, ('#f1f5f9', '#334155', obj.get_stream_display()))
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:999px;font-weight:600;font-size:0.78rem;display:inline-block;">{}</span>',
            bg, fg, label
        )


# Setup for Students
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('name', 'grade', 'stream', 'parent_phone')
        import_id_fields = ('name',)


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = ('name', 'grade', 'stream', 'parent_phone')
    search_fields = ('name', 'grade', 'stream')
    list_filter = ('grade', 'stream')
    filter_horizontal = ('subjects',)

    class Media:
        js = ('academics/js/student_stream_subjects.js',)


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


# --- UPDATED RESULT ADMIN (SHOWS STUDENT ID & SUBJECT) ---

@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ('get_student_id', 'get_student_name', 'subject_ref', 'subject', 'score_badge', 'exam_date')
    list_filter = ('subject_ref__grade', 'subject_ref__stream', 'subject', 'exam_date')
    search_fields = ('student__student_id', 'student__first_name', 'student__last_name', 'subject', 'subject_ref__name')
    autocomplete_fields = ('subject_ref',)
    list_per_page = 30

    @admin.display(description='Student ID', ordering='student__student_id')
    def get_student_id(self, obj):
        return obj.student.student_id

    @admin.display(description='Student Name')
    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"

    @admin.display(description='Score', ordering='score')
    def score_badge(self, obj):
        val = float(obj.score)
        if val >= 85:
            bg, fg = ('#dcfce7', '#15803d')
        elif val >= 50:
            bg, fg = ('#e0f2fe', '#0369a1')
        else:
            bg, fg = ('#fee2e2', '#b91c1c')
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:999px;font-weight:700;font-size:0.82rem;display:inline-block;">{}</span>',
            bg, fg, obj.score
        )


# --- SCHOOL ADMIN BRANDING ---
admin.site.site_header = "Chercher SS Administration"
admin.site.site_title = "Chercher SS Admin"
admin.site.index_title = "Dashboard"