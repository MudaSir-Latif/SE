from django import forms
from .models import student

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = student
        fields = ['user','full_name', 'email', 'date_of_birth','course_name','type']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
