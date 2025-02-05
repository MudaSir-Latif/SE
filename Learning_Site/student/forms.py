from django import forms
from .models import Student

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'email', 'date_of_birth', 'course_name', 'type', 'payment_method', 'payment_screenshot']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),  # Added widget for Full Name
            'email': forms.EmailInput(attrs={'class': 'form-control'}),     # Added widget for Email
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'payment_screenshot': forms.FileInput(attrs={'class': 'form-control'}),
        }
    