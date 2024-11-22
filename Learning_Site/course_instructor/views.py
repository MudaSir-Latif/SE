from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse
from django.db.models import Prefetch
from django.forms import formset_factory
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView
from .models import (
    Course, CourseContent, Purchase, Profile, VideoWatch, Quiz, Question
)
from .forms import (
    CourseForm, CourseContentForm, QuizForm, QuestionForm
)
import json

# Create a new course (Instructor only)
@login_required(login_url='registration/login/')
def create_course(request):
    if not request.user.profile.is_instructor:
        raise PermissionDenied("You must be an instructor to create a course.")
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user.profile  # Link the course to the instructor
            course.save()
            return redirect('course_details')  # Redirect to the course details page
    else:
        form = CourseForm()

    return render(request, 'registration/create_course.html', {'form': form})

# Filter courses by type (paid/unpaid/all)
def filter_courses(request):
    course_type = request.GET.get('type', 'all')
    content_prefetch = Prefetch(
        'contents',
        queryset=CourseContent.objects.all().order_by('order')
    )
    if course_type == 'paid':
        courses = Course.objects.filter(course_type='paid').prefetch_related(content_prefetch)
    elif course_type == 'unpaid':
        courses = Course.objects.filter(course_type='unpaid').prefetch_related(content_prefetch)
    else:
        courses = Course.objects.all().prefetch_related(content_prefetch)

    return render(request, 'course_list.html', {'courses': courses, 'selected_type': course_type})


# Add or update course content
@login_required(login_url='registration/login/')
def add_update_content(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = CourseContentForm(request.POST, request.FILES)
        if form.is_valid():
            course_content = form.save(commit=False)
            course_content.course = course
            course_content.save()
            return redirect('success_page')
        else:
            print(form.errors)
    else:
        form = CourseContentForm()

    return render(request, 'registration/add_content.html', {'form': form, 'course': course})

# Custom login view for instructors
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        if user.profile.is_instructor:
            login(self.request, user)
            return redirect('create_course')
        else:
            raise PermissionDenied("You must be an instructor to access this page.")

# Mark a video as watched
@csrf_exempt
def mark_video_watched(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            video_id = data.get('video_id')
            student_id = data.get('student_id')

            video_content = CourseContent.objects.get(id=video_id)
            student = User.objects.get(id=student_id)

            video_watch, _ = VideoWatch.objects.get_or_create(
                student=student,
                video_content=video_content
            )
            video_watch.watched = True
            video_watch.watched_at = timezone.now()
            video_watch.save()

            return JsonResponse({'status': 'success'}, status=200)
        except CourseContent.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Video not found'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)

# Quiz view for students
@login_required
def quiz_view(request, content_id):
    content = get_object_or_404(CourseContent, id=content_id)
    quiz = get_object_or_404(Quiz, course_content=content)
    
    if request.method == "POST":
        answers = request.POST.dict()
        correct_count = sum(
            1 for question in quiz.questions.all()
            if question.check_answer(answers.get(f'question_{question.id}'))
        )
        return render(request, 'quiz_result.html', {
            'correct_count': correct_count,
            'total_questions': quiz.questions.count(),
        })

    return render(request, 'quiz.html', {'quiz': quiz})

# Create a quiz and associated questions
@login_required(login_url='registration/login/')
def create_quiz(request, video_id):
    course_content = get_object_or_404(CourseContent, id=video_id, content_type='video')
    if hasattr(course_content, 'quiz'):
        return JsonResponse({'message': 'Quiz already exists for this video.'}, status=400)
    
    QuestionFormSet = formset_factory(QuestionForm, extra=10)

    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST)

        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.course_content = course_content
            quiz.save()

            for form in question_formset:
                question = form.save(commit=False)
                question.quiz = quiz
                question.save()

            return redirect('course_detail', course_content.id)
    else:
        quiz_form = QuizForm(initial={'title': f"Quiz for {course_content.title}"})
        question_formset = QuestionFormSet()

    return render(
        request, 
        'registration/create_quiz.html', 
        {'quiz_form': quiz_form, 'question_formset': question_formset, 'course_content': course_content}
    )
