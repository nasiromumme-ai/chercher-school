from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from documents.models import Document
from core.models import News, Gallery
from academics.models import Student, Teacher
from admissions.models import Application # Assuming you have an Application model

@login_required
def index(request):
    context = {
        'total_documents': Document.objects.count(),
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'total_news': News.objects.count(),
        'recent_documents': Document.objects.all()[:5],
    }
    return render(request, 'dashboard/index.html', context)

class CustomLoginView(LoginView):
    template_name = 'dashboard/login.html'

# --- STUDENTS ---
@login_required
def manage_students(request):
    students = Student.objects.all()
    return render(request, 'dashboard/manage_students.html', {'students': students})

@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('dashboard:manage_students')

# --- TEACHERS ---
@login_required
def manage_teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'dashboard/manage_teachers.html', {'teachers': teachers})

@login_required
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.delete()
    return redirect('dashboard:manage_teachers')

# --- NEWS ---
@login_required
def manage_news(request):
    news_list = News.objects.all().order_by('-created_at')
    return render(request, 'dashboard/manage_news.html', {'news_list': news_list})

@login_required
def delete_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    news.delete()
    return redirect('dashboard:manage_news')

# --- GALLERY ---
@login_required
def manage_gallery(request):
    images = Gallery.objects.all().order_by('-uploaded_at')
    return render(request, 'dashboard/manage_gallery.html', {'images': images})

@login_required
def delete_gallery(request, image_id):
    image = get_object_or_404(Gallery, id=image_id)
    image.delete()
    return redirect('dashboard:manage_gallery')

# --- DOCUMENTS ---
@login_required
def manage_documents(request):
    documents = Document.objects.all().order_by('-uploaded_at')
    return render(request, 'dashboard/manage_documents.html', {'documents': documents})

@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.delete()
    return redirect('dashboard:manage_documents')

# --- USERS ---
@login_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'dashboard/manage_users.html', {'users': users})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user: 
        user.delete()
    return redirect('dashboard:manage_users')