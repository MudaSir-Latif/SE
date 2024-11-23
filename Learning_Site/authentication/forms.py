# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, CreatorProfile

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPES, required=True)

    # Extra fields for student and creator
    age = forms.IntegerField(required=False, help_text="For students")
    experience = forms.IntegerField(required=False, help_text="For creators (years of experience)")
    course_type = forms.CharField(required=False, help_text="For creators (type of courses)")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if user.user_type == 'student':
                # Create the StudentProfile when user type is 'student'
                StudentProfile.objects.create(user=user, age=self.cleaned_data.get('age'))
            elif user.user_type == 'creator':
                # Create the CreatorProfile when user type is 'creator'
                CreatorProfile.objects.create(
                    user=user,
                    experience=self.cleaned_data.get('experience'),
                    course_type=self.cleaned_data.get('course_type'),
                )
        return user
