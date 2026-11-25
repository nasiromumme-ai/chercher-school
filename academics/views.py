from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render
from .models import Teacher, Student, StudentResult, Subject
from .services import get_available_classes, compute_class_standings
from registration.models import RegisteredStudent


def teacher_list(request):
    teachers = Teacher.objects.all()
    department = request.GET.get('department')

    if department:
        teachers = teachers.filter(department=department)

    departments = Teacher.objects.values_list('department', flat=True).distinct().exclude(department='')

    return render(request, 'academics/teachers.html', {
        'teachers': teachers,
        'departments': departments,
        'selected_department': department
    })


def student_list(request):
    students = Student.objects.all()
    return render(request, 'academics/students.html', {'students': students})


# --- SEMESTER 1 & 2 RESULT CHECKER + CLASS RANKINGS ---

def check_result(request):
    results = None
    student_id = ''
    registered_student = None
    student_summary = None
    class_standings = None
    error = None

    academic_year = (request.POST.get('year') or request.GET.get('year') or '').strip() or None
    selected_class = (request.GET.get('class_name') or '').strip().upper()
    available_classes = get_available_classes(academic_year=academic_year)

    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        if student_id:
            registered_student = RegisteredStudent.objects.filter(student_id__iexact=student_id).first()

            if registered_student:
                qs = StudentResult.objects.filter(student=registered_student).select_related('subject_ref')
                if academic_year:
                    qs = qs.filter(academic_year=academic_year)
                results = qs

                if results.exists():
                    latest_res = results.order_by('-academic_year', '-id').first()
                    stu_class = latest_res.class_label
                    stu_year = latest_res.academic_year or academic_year

                    if stu_class and stu_class != "Unassigned":
                        class_standings = compute_class_standings(stu_class, academic_year=stu_year)
                        selected_class = stu_class
                        for row in class_standings['students']:
                            if row['student'].id == registered_student.id:
                                row['total_in_class'] = class_standings['total_in_class']
                                row['class_label'] = stu_class
                                row['subject_avg_map'] = class_standings['subject_avg_map']
                                student_summary = row
                                break
                else:
                    error = "No exam results found for this Student ID yet."
            else:
                error = "Student ID not found. Please check the ID and try again."
        else:
            error = "Please enter a valid Student ID."

    elif selected_class:
        class_standings = compute_class_standings(selected_class, academic_year=academic_year)
        if class_standings['total_in_class'] == 0:
            error = f"No results recorded for class {selected_class} yet."

    return render(request, 'academics/check_result.html', {
        'results': results,
        'student_id': student_id,
        'registered_student': registered_student,
        'student_summary': student_summary,
        'class_standings': class_standings,
        'selected_class': selected_class,
        'available_classes': available_classes,
        'academic_year': academic_year or '',
        'error': error,
    })


def class_rankings(request, class_name=None):
    academic_year = (request.GET.get('year') or '').strip() or None
    available_classes = get_available_classes(academic_year=academic_year)

    selected_class = (
        class_name
        or request.GET.get('class_name')
        or (available_classes[0] if available_classes else '')
    ).strip().upper()

    class_standings = None
    error = None

    if selected_class:
        class_standings = compute_class_standings(selected_class, academic_year=academic_year)
        if class_standings['total_in_class'] == 0:
            error = f"No results recorded for class {selected_class} yet."
    else:
        error = "No class results recorded yet."

    return render(request, 'academics/check_result.html', {
        'results': None,
        'student_id': '',
        'registered_student': None,
        'student_summary': None,
        'class_standings': class_standings,
        'selected_class': selected_class,
        'available_classes': available_classes,
        'academic_year': academic_year or '',
        'error': error,
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