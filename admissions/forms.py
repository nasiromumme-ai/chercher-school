from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['student_name', 'parent_name', 'email', 'phone', 'previous_school', 'grade_applying', 'message']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student Full Name'}),
            'parent_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent/Guardian Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'previous_school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Previous School'}),
            'grade_applying': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Grade Applying For (e.g., Grade 9)'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any additional information'}),
        }