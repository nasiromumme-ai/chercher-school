from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.db import models
from documents.models import Document
from core.models import News, Gallery
from academics.models import Student, Teacher
from admissions.models import Application
from registration.models import RegisteredStudent
from registration.forms import RegistrationForm
from reports.models import MonthlyReport  # <--- IMPORT ADDED HERE

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

# --- STUDENT REGISTRATION (WITH SEARCH FILTERS) ---

@login_required
def manage_registrations(request):
    students = RegisteredStudent.objects.all()
    
    # Get search parameters from the URL
    grade = request.GET.get('grade')
    program = request.GET.get('program')
    gender = request.GET.get('gender')
    search_query = request.GET.get('search_query')
    
    # Apply filters
    if grade:
        students = students.filter(grade=grade)
    if program:
        students = students.filter(program=program)
    if gender:
        students = students.filter(gender=gender)
    if search_query:
        # Search by first name, last name, or student ID
        students = students.filter(
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query) |
            models.Q(student_id__icontains=search_query)
        )
        
    return render(request, 'dashboard/manage_registrations.html', {
        'students': students,
        'selected_grade': grade,
        'selected_program': program,
        'selected_gender': gender,
        'search_query': search_query,
    })

@login_required
def add_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:manage_registrations')
    else:
        form = RegistrationForm()
    return render(request, 'dashboard/add_registration.html', {'form': form})

@login_required
def edit_registration(request, pk):
    student = get_object_or_404(RegisteredStudent, pk=pk)
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('dashboard:manage_registrations')
    else:
        form = RegistrationForm(instance=student)
    return render(request, 'dashboard/add_registration.html', {'form': form})

@login_required
def delete_registration(request, pk):
    student = get_object_or_404(RegisteredStudent, pk=pk)
    student.delete()
    return redirect('dashboard:manage_registrations')

# --- VIEW REGISTRATION ---

@login_required
def view_registration(request, pk):
    student = get_object_or_404(RegisteredStudent, pk=pk)
    return render(request, 'dashboard/view_registration.html', {'student': student})

# --- MONTHLY REPORTS (NEW) ---

@login_required
def manage_reports(request):
    reports = MonthlyReport.objects.all()
    
    # Filters
    month = request.GET.get('month')
    year = request.GET.get('year')
    grade = request.GET.get('grade')
    
    if month:
        reports = reports.filter(month=month)
    if year:
        reports = reports.filter(year=year)
    if grade:
        reports = reports.filter(grade__icontains=grade)
        
    # Get unique years for filter
    years = MonthlyReport.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    return render(request, 'dashboard/manage_reports.html', {
        'reports': reports,
        'selected_month': month,
        'selected_year': year,
        'selected_grade': grade,
        'years': years,
    })

@login_required
def delete_report(request, report_id):
    report = get_object_or_404(MonthlyReport, id=report_id)
    report.delete()
    return redirect('dashboard:manage_reports')