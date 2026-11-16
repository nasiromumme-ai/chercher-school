from django.shortcuts import render
from .models import Teacher, Student

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'academics/teachers.html', {'teachers': teachers})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'academics/students.html', {'students': students})