from django import forms
from course_instructor.models import Course, CourseContent
from .models import Quiz

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'duration']  # Fields to be edited by the instructor


class CourseContentForm(forms.ModelForm):
    class Meta:
        model = CourseContent
        fields = ['title', 'video', 'content_type', 'order', 'additional_resources']

# from django import forms
# from .models import Quiz, Question

# class QuizForm(forms.Form):
#     """
#     Form for rendering quiz questions with options.
#     """

#     def __init__(self, *args, **kwargs):
#         quiz = kwargs.pop('quiz')  # Passing the quiz dynamically
#         super().__init__(*args, **kwargs)

#         # Dynamically add fields for each question in the quiz
#         for i, question in enumerate(quiz.questions.all()):
#             # Create a form field for each question
#             field_name = f'question_{i}'
#             self.fields[field_name] = forms.ChoiceField(
#                 choices=[('a', question.option_a),
#                          ('b', question.option_b),
#                          ('c', question.option_c),
#                          ('d', question.option_d)],
#                 label=question.question_text,
#                 widget=forms.RadioSelect,
#                 required=True  # Make sure the question must be answered
#             )
    
#     def clean(self):
#         """
#         Perform any additional validation if needed.
#         """
#         cleaned_data = super().clean()
#         # You can add more checks here if required
#         return cleaned_data
from django import forms
from .models import Quiz, Question

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
