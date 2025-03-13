from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from course_instructor.models import Course, CourseContent

# def if_is_instructor(request):
#     return render(request, "if_is_instructor.html")

from django.contrib.auth.decorators import login_required

@login_required
def main_page(request):
    query = request.GET.get('q', '').strip()  # Get the search query from the URL, strip whitespace
    if request.user.profile_main.role == 'instructor':
        # Fetch only courses created by the logged-in instructor
        courses = Course.objects.filter(instructor=request.user)
    else:
        courses = Course.objects.all()
    
    # Filter courses only if there is a query
    if query:
        courses = courses.filter(title__icontains=query)

    return render(request, 'main_page.html', {'courses': courses, 'query': query})

from student.models import Subscription



def User_Profile(request):
    if request.user.profile_main.role == 'learner':
        # Get courses directly related to the user's subscriptions
        courses = Course.objects.filter(subscription__user=request.user).distinct()
    else:
        # For other roles, show all courses
        courses = Course.objects.all()

    return render(request, 'profile.html', {'courses': courses})


