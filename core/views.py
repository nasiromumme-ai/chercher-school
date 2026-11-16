from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import News, Gallery, TopStudent, SchoolStructure, ContactMessage, Event # <-- Event added here
from .forms import ContactForm
from academics.models import Student, Teacher

def home(request):
    latest_news = News.objects.all().order_by('-created_at')[:3]
    top_students = TopStudent.objects.all()[:4]
    
    # Get the Director's info for the homepage
    director = SchoolStructure.objects.filter(role__icontains='Director').first()
    
    # Get the total counts
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    
    return render(request, 'core/home.html', {
        'latest_news': latest_news,
        'top_students': top_students,
        'director': director,
        'total_students': total_students,
        'total_teachers': total_teachers,
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

# --- NEW EVENT VIEW ADDED BELOW ---

def events(request):
    upcoming_events = Event.objects.all().order_by('date')
    return render(request, 'core/events.html', {'events': upcoming_events})