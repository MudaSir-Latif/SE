from django import forms
from course_instructor.models import Course, CourseContent
from .models import Quiz, Question

class CourseForm(forms.ModelForm):
    duration = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in days'}),
        label="Duration (Days)"
    )

    class Meta:
        model = Course
        fields = ['title', 'description', 'course_type', 'duration', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Enter course description'}),
            'course_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter course price'}),
        }

    def clean_duration(self):
        days = self.cleaned_data.get('duration')
        if days is not None:
            return timedelta(days=days)  # Convert integer to timedelta
        return timedelta(days=30)  # Default value if not provided

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.duration = self.cleaned_data['duration']  # Ensure duration is set
        if commit:
            instance.save()
        return instance

class CourseContentForm(forms.ModelForm):
    class Meta:
        model = CourseContent
        fields = ['Contenttitle', 'video', 'content_type', 'order', 'additional_resources', 'is_last_video']
        widgets = {
            'Contenttitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter content title'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
            'content_type': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter content order'}),
            'additional_resources': forms.FileInput(attrs={'class': 'form-control'}),
            'is_last_video': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = ['title']
        widgets = {
            'question_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter question text'}),
            'option_a': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter option A'}),
            'option_b': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter option B'}),
            'option_c': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter option C'}),
            'option_d': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter option D'}),
            'correct_answer': forms.Select(attrs={'class': 'form-control'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
        widgets = {
            'question_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter question text'}),
            'option_a': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter option A'}),
            'option_b': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter option B'}),
            'option_c': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter option C'}),
            'option_d': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter option D'}),
            'correct_answer': forms.Select(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import CourseFeedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        fields = ['video_quality', 'audio_quality', 'teaching_method', 'course_content', 'feedback']
        widgets = {
            'video_quality': forms.Select(attrs={'class': 'form-control'}),
            'audio_quality': forms.Select(attrs={'class': 'form-control'}),
            'teaching_method': forms.Select(attrs={'class': 'form-control'}),
            'course_content': forms.Select(attrs={'class': 'form-control'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your feedback here...'}),
        }
