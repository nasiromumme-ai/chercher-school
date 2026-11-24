import mimetypes
import os
from django.http import FileResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import (
    News,
    Gallery,
    TopStudent,
    SchoolStructure,
    ContactMessage,
    Event,
    Subscriber,
    SchoolHighlight,
)
from .forms import ContactForm
from academics.models import Student, Teacher
from reports.models import MonthlyReport


def home(request):
    latest_news = News.objects.all().order_by('-created_at')[:6]
    top_students = TopStudent.objects.all()[:4]

    director = SchoolStructure.objects.filter(role__icontains='Director').first()

    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()

    meeting_photos = SchoolHighlight.objects.filter(
        is_published=True,
        category__in=['weekly_meeting', 'monthly_meeting'],
    ).order_by('-date_recorded', '-id')[:12]

    staff_decisions = SchoolHighlight.objects.filter(
        is_published=True,
        category='staff_decision',
    ).order_by('-date_recorded', '-id')[:12]

    cooperation_posts = SchoolHighlight.objects.filter(
        is_published=True,
        category='student_cooperation',
    ).order_by('-date_recorded', '-id')[:12]

    return render(request, 'core/home.html', {
        'latest_news': latest_news,
        'top_students': top_students,
        'director': director,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'meeting_photos': meeting_photos,
        'staff_decisions': staff_decisions,
        'cooperation_posts': cooperation_posts,
    })


def about(request):
    director = SchoolStructure.objects.filter(role__icontains='Director').first()
    structure = SchoolStructure.objects.exclude(role__icontains='Director')
    top_students = TopStudent.objects.all()

    return render(request, 'core/about.html', {
        'director': director,
        'structure': structure,
        'top_students': top_students
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'core/contact.html', {'form': ContactForm(), 'success': True})
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})


def gallery(request):
    images = Gallery.objects.all().order_by('-uploaded_at')
    return render(request, 'core/gallery.html', {'images': images})


def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'core/news_detail.html', {'news': news_item})


def logout_view(request):
    logout(request)
    return redirect('/')


# --- NEW EVENT VIEW ---

def events(request):
    upcoming_events = Event.objects.all().order_by('date')
    return render(request, 'core/events.html', {'events': upcoming_events})


# --- NEW DOWNLOADS VIEW ---

def downloads(request):
    return render(request, 'core/downloads.html')


# --- NEW SUBSCRIBE VIEW ---

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            Subscriber.objects.get_or_create(email=email)
            return redirect('/?subscribed=True')
    return redirect('/')


# --- NEW PUBLIC REPORTS VIEW ---

def public_reports(request):
    reports = MonthlyReport.objects.all().order_by('-uploaded_at', '-id')

    month = request.GET.get('month')
    year = request.GET.get('year')

    if month:
        reports = reports.filter(month=month)
    if year:
        reports = reports.filter(year=year)

    years = MonthlyReport.objects.values_list('year', flat=True).distinct().order_by('-year')

    return render(request, 'core/public_reports.html', {
        'reports': reports,
        'selected_month': month,
        'selected_year': year,
        'years': years,
    })


def view_report(request, report_id):
    report = get_object_or_404(MonthlyReport, id=report_id)
    if not report.file:
        raise Http404("Report file not found.")

    filename = os.path.basename(report.file.name).lower()
    if filename.endswith(('.pdf', '.png', '.jpg', '.jpeg', '.gif', '.webp')):
        content_type, _ = mimetypes.guess_type(report.file.name)
        response = FileResponse(
            report.file.open('rb'),
            as_attachment=False,
            content_type=content_type or 'application/pdf',
        )
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(report.file.name)}"'
        return response

    return render(request, 'core/report_reader.html', {'report': report})


def download_report(request, report_id):
    report = get_object_or_404(MonthlyReport, id=report_id)
    if not report.file:
        raise Http404("Report file not found.")

    if not report.allow_download:
        return HttpResponseForbidden(
            "Downloads are currently disabled for this report. You may view it on the report page."
        )

    return FileResponse(
        report.file.open('rb'),
        as_attachment=True,
        filename=os.path.basename(report.file.name),
    )