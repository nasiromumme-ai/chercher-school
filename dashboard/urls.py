from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    
    # Students
    path('students/', views.manage_students, name='manage_students'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    
    # Teachers
    path('teachers/', views.manage_teachers, name='manage_teachers'),
    path('teachers/delete/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    
    # News
    path('news/', views.manage_news, name='manage_news'),
    path('news/delete/<int:news_id>/', views.delete_news, name='delete_news'),
    
    # Gallery
    path('gallery/', views.manage_gallery, name='manage_gallery'),
    path('gallery/delete/<int:image_id>/', views.delete_gallery, name='delete_gallery'),
    
    # Documents
    path('documents/', views.manage_documents, name='manage_documents'),
    path('documents/delete/<int:document_id>/', views.delete_document, name='delete_document'),
    
    # Users
    path('users/', views.manage_users, name='manage_users'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]