from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render
from .models import Teacher, Student, StudentResult, Subject
from registration.models import RegisteredStudent


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


# --- SIMPLIFIED RESULT CHECKER VIEW ---

def check_result(request):
    results = None
    student_id = None
    error = None

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        if student_id:
            # 1. Find the Registered Student by their ID
            registered_student = RegisteredStudent.objects.filter(student_id=student_id).first()

            if registered_student:
                # 2. Get all results linked to this exact student ID
                results = StudentResult.objects.filter(student=registered_student)
                if not results:
                    error = "No exam results found for this Student ID yet."
            else:
                error = "Student ID not found. Please check the ID and try again."

    return render(request, 'academics/check_result.html', {
        'results': results,
        'student_id': student_id,
        'error': error
    })


# --- ADMIN AUTO-SELECT SUBJECTS BY GRADE & STREAM ---

@staff_member_required
def admin_subjects_for_grade_stream(request):
    raw_grade = request.GET.get("grade", "")
    stream = request.GET.get("stream", "Common")

    grade_num = "".join(ch for ch in str(raw_grade) if ch.isdigit())
    if grade_num not in ["9", "10", "11", "12"]:
        return JsonResponse({"subject_ids": []})

    if grade_num in ["9", "10"]:
        qs = Subject.objects.filter(grade=grade_num, stream="Common")
    else:
        stream_val = stream if stream in ["Natural", "Social"] else "Common"
        qs = Subject.objects.filter(grade=grade_num, stream=stream_val)

    return JsonResponse({
        "subject_ids": list(qs.values_list("id", flat=True))
    })