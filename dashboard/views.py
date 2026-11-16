from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from documents.models import Document
from core.models import News, Gallery
from academics.models import Student, Teacher
from django.contrib.auth.views import LoginView

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