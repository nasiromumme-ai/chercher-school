from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('teachers/', views.teacher_list, name='teachers'),
    path('students/', views.student_list, name='students'),
]