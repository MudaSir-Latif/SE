from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Course, CourseContent
from .forms import CourseForm, CourseContentForm
from .models import Purchase,Profile,Course,CourseContent,VideoWatch
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied

from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

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
            return redirect('course_details')  # Redirect to the course details page or list
    else:
        form = CourseForm()

    return render(request, 'registration/create_course.html', {'form': form})



 # Assuming Course is the model for courses

@login_required(login_url='registration/login/')
def add_update_content(request, course_id):
    course = get_object_or_404(Course, id=course_id)  # Retrieve the course using the course_id
    if request.method == "POST":
        form = CourseContentForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the content but associate it with the retrieved course
            course_content = form.save(commit=False)
            course_content.course = course  # Associate the course with the content
            course_content.save()
            return redirect('success_page')  # Redirect after saving
        else:
            print(form.errors)
    else:
        form = CourseContentForm()

    return render(request, 'registration/add_content.html', {'form': form, 'course': course})



class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True  # If the user is already logged in, redirect them

    def form_valid(self, form):
        # Authenticate the user and check if they are an instructor
        user = form.get_user()

        if user.profile.is_instructor:  # Check if the user is an instructor
            login(self.request, user)  # Log the user in
            return redirect('create_course')  # Redirect to create_course view
        else:
            raise PermissionDenied("You must be an instructor to access this page.")



# from course_details.models import Enrollment



# @login_required(login_url='registration/login/')
# def buy_course(request, course_id):
#     # Fetch the course based on the provided course_id
#     course = get_object_or_404(Course, id=course_id)

#     # Check if the user has already bought the course
#     if Purchase.objects.filter(student=request.user.profile, course=course).exists():
#         messages.error(request, "You have already purchased this course.")
#         return redirect('registration/course_details', course_id=course.id)

#     # Create a purchase record
#     purchase = Purchase.objects.create(student=request.user.profile, course=course)
    
#     # Automatically enroll the user in the course after purchase
#     if not Enrollment.objects.filter(student=request.user.profile, course=course).exists():
#         Enrollment.objects.create(student=request.user.profile, course=course)

#     # Success message and redirect to course details page
#     messages.success(request, f"You have successfully purchased and enrolled in {course.title}!")
#     return redirect('registration/course_details', course_id=course.id)





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CourseContent, VideoWatch
from django.utils import timezone
import json
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CourseContent, VideoWatch
from django.utils import timezone
import json
from django.urls import reverse
from django.utils.timezone import now  # Ensuring the timezone is imported for watched_at

@csrf_exempt
def mark_video_watched(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            video_id = data.get('video_id')
            student_id = data.get('student_id')

            # Find the video content by ID
            video_content = CourseContent.objects.get(id=video_id)
            student = User.objects.get(id=student_id)

            # Update the 'watched' status in the VideoWatch table
            video_watch, created = VideoWatch.objects.get_or_create(
                student=student,
                video_content=video_content
            )
            video_watch.watched = True
            video_watch.watched_at = timezone.now()  # Set the time when it was watched
            video_watch.save()

            return JsonResponse({'status': 'success'}, status=200)
            

        except CourseContent.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Video not found'}, status=404)

        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400) 
            # Check for an associated quiz
            # quiz = Quiz.objects.filter(course_content=video_content).first()
            # if quiz:
            #     quiz_url = reverse('quiz_view', args=[video_content.id])  # Adjust 'quiz_view' to match your URL name
            #     return JsonResponse({'status': 'success', 'quiz_url': quiz_url}, status=200)

            # # If no quiz is associated, return success without quiz URL
            # return JsonResponse({'status': 'success', 'message': 'Video marked as watched, no quiz available.'}, status=200)

            



# @csrf_exempt
# def mark_video_watched(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             video_id = data.get('video_id')
#             student_id = data.get('student_id')

#             # Find the video content by ID
#             video_content = CourseContent.objects.get(id=video_id)
#             student = User.objects.get(id=student_id)

#             # Check if the video has already been marked as watched
#             video_watch, created = VideoWatch.objects.get_or_create(
#                 student=student,
#                 video_content=video_content
#             )
            
#             if not video_watch.watched:  # Only update if it's not already marked as watched
#                 video_watch.watched = True
#                 video_watch.watched_at = timezone.now()  # Set the time when it was watched
#                 video_watch.save()

#             return JsonResponse({'status': 'success'}, status=200)

#         except CourseContent.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Video not found'}, status=404)

#         except User.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)

#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)




# def quiz_view(request, content_id):
#     content = get_object_or_404(CourseContent, id=content_id)
#     quiz = get_object_or_404(Quiz, course_content=content)

#     if request.method == "POST":
#         answers = request.POST.dict()
#         correct_count = 0
#         for question in quiz.questions.all():
#             user_answer = answers.get(f'question_{question.id}')
#             if question.check_answer(user_answer):
#                 correct_count += 1

#         return render(request, 'quiz_result.html', {'correct_count': correct_count, 'total_questions': quiz.questions.count()})

#     return render(request, 'registration/quiz.html', {'quiz': quiz})
@login_required
def quiz_view(request, content_id):
    content = get_object_or_404(CourseContent, id=content_id)
    quiz = get_object_or_404(Quiz, course_content=content)
    
    if request.method == "POST":
        answers = request.POST.dict()
        correct_count = 0
        for question in quiz.questions.all():
            user_answer = answers.get(f'question_{question.id}')
            if question.check_answer(user_answer):
                correct_count += 1

        return render(request, 'quiz_result.html', {
            'correct_count': correct_count,
            'total_questions': quiz.questions.count(),
        })

    return render(request, 'quiz.html', {'quiz': quiz})


# from .models import Quiz
# from .forms import QuizForm, QuestionForm


# def create_quiz(request, content_id):
#     content = get_object_or_404(CourseContent, id=content_id)

#     if request.method == "POST":
#         quiz_form = QuizForm(request.POST)
#         if quiz_form.is_valid():
#             quiz = quiz_form.save(commit=False)
#             quiz.course_content = content
#             quiz.save()
#             return redirect('add_questions', quiz_id=quiz.id)
#     else:
#         quiz_form = QuizForm()

#     return render(request, 'registration/create_quiz.html', {'quiz_form': quiz_form, 'content': content})
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from .models import CourseContent, Quiz, Question
from .forms import QuizForm, QuestionForm


@login_required(login_url='registration/login/')
def create_quiz(request, video_id):
    # Get the CourseContent object
    course_content = get_object_or_404(CourseContent, id=video_id, content_type='video')
    
    # Check if the quiz already exists
    if hasattr(course_content, 'quiz'):
        return JsonResponse({'message': 'Quiz already exists for this video.'}, status=400)
    
    # Initialize the question formset
    QuestionFormSet = formset_factory(QuestionForm, extra=10)

    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST)

        if quiz_form.is_valid() and question_formset.is_valid():
            # Save the quiz
            quiz = quiz_form.save(commit=False)
            quiz.course_content = course_content
            quiz.save()  # Save the quiz to assign a primary key

            # Save all valid questions and link them to the quiz
            for form in question_formset:
                question = form.save(commit=False)
                question.quiz = quiz  # Now you can assign quiz because it has a primary key
                question.save()  # Save the question to the database

            return redirect('course_detail', course_content.id)  # Redirect after quiz creation
        else:
            # Render the form with errors if the forms are not valid
            return render(
                request, 
                'create_quiz.html', 
                {'quiz_form': quiz_form, 'question_formset': question_formset, 'course_content': course_content}
            )
    else:
        # Initialize empty forms for the quiz and questions
        quiz_form = QuizForm(initial={'title': f"Quiz for {course_content.title}"})
        question_formset = QuestionFormSet()

    return render(
        request, 
        'registration/create_quiz.html', 
        {'quiz_form': quiz_form, 'question_formset': question_formset, 'course_content': course_content}
    )






def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            if quiz.questions.count() == 10:
                return redirect('quiz_success')  # Redirect after all 10 questions are added
            return redirect('add_questions', quiz_id=quiz.id)
    else:
        question_form = QuestionForm()

    return render(request, 'registration/add_questions.html', {'question_form': question_form, 'quiz': quiz})
