from django.shortcuts import render
from .models import Alumni

def alumni_list(request):
    alumni = Alumni.objects.all()
    return render(request, 'alumni/alumni_list.html', {'alumni': alumni})