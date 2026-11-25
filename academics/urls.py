from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('teachers/', views.teacher_list, name='teachers'),
    path('students/', views.student_list, name='students'),
    path('check-result/', views.check_result, name='check_result'),
    path('class-rankings/', views.class_rankings, name='class_rankings'),
    path('class-rankings/<str:class_name>/', views.class_rankings, name='class_rankings_detail'),
    path(
        'admin/subjects-for-grade-stream/',
        views.admin_subjects_for_grade_stream,
        name='admin_subjects_for_grade_stream',
    ),
]