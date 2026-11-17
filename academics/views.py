from django.shortcuts import render
from .models import Teacher, Student, StudentResult

def teacher_list(request):
    teachers = Teacher.objects.all()
    department = request.GET.get('department')
    
    if department:
        teachers = teachers.filter(department=department)
        
    # Get unique departments for the filter buttons
    departments = Teacher.objects.values_list('department', flat=True).distinct().exclude(department='')
    
    return render(request, 'academics/teachers.html', {
        'teachers': teachers,
        'departments': departments,
        'selected_department': department
    })

def student_list(request):
    students = Student.objects.all()
    return render(request, 'academics/students.html', {'students': students})

# --- NEW RESULT CHECKER VIEW ADDED BELOW ---

def check_result(request):
    results = None
    student_name = None
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        if student_name:
            # Basic search by name (you can make this use a unique ID later)
            student = Student.objects.filter(name__iexact=student_name).first()
            if student:
                results = StudentResult.objects.filter(student=student)
    
    return render(request, 'academics/check_result.html', {'results': results, 'student_name': student_name})