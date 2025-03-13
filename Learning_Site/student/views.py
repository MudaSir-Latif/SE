from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Subscription
from .forms import SubscriptionForm
from course_instructor.models import Course
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def unpaid_courses(request):
    return render(request, 'content.html')

def paid_courses(request):
    return render(request, 'content.html')

@login_required
def subscribe(request, course_name, course_type):
    print(f"Course Name: {course_name}, Course Type: {course_type}")  # Debugging line

    if request.method == 'POST':
        form = SubscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid, saving...")  # Debugging line
            student_data = form.save(commit=False)  # Get the student instance
            
            if request.user.is_authenticated:
                student_data.user = request.user
            
            student_data.course_name = course_name
            student_data.type = course_type
            
            if course_type == 'paid':
                if not student_data.payment_method:
                    form.add_error('payment_method', 'Payment method is required for paid courses.')
                payment_screenshot = request.FILES.get('payment_screenshot')
                if not payment_screenshot:
                    form.add_error('payment_screenshot', 'Payment screenshot is required for paid courses.')
                else:
                    student_data.payment_screenshot = payment_screenshot
            
            if not form.errors:
                student_data.save()
                print("Student data saved successfully.")

                # Fetch course instance
                try:
                    course_instance = Course.objects.get(title=course_name)
                except Course.DoesNotExist:
                    return render(request, 'subscribe.html', {'error': 'Course not found'})

                # Save subscription details
                subscription = Subscription(
                    user=student_data.user,
                    student=student_data,
                    course=course_instance,
                )
                subscription.save()
                print("Subscription saved successfully.")
                
                return render(request, 'subscribe.html', {'subscription_success': True, 'course_name': course_name})
            else:
                print(f"Form errors: {form.errors}")
        else:
            print(f"Form is invalid: {form.errors}")
    else:
        form = SubscriptionForm(initial={'course_name': course_name, 'type': course_type})

    return render(request, 'subscribe.html', {'form': form, 'course_name': course_name, 'course_type': course_type})

def home(request):
    return render(request,'content.html')
