from django.shortcuts import render
from .models import Document

def document_list(request):
    documents = Document.objects.all()
    return render(request, 'documents/list.html', {'documents': documents})