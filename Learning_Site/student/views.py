from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Subscription
from .forms import SubscriptionForm
from course_instructor.models import Course

def unpaid_courses(request):
    return render(request, 'content.html')

def paid_courses(request):
    return render(request, 'content.html')

def subscribe(request, course_name, course_type):
    print(f"Course Name: {course_name}, Course Type: {course_type}")  # Debugging line

    if request.method == 'POST':
        form = SubscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid, saving...")  # Debugging line
            student_data = form.save(commit=False)  # Get the student instance
            
            # Assign the logged-in user if available
            #if request.user.is_authenticated:
             #    student_data.user = request.user
            
            student_data.course_name = course_name  # Set course_name automatically
            student_data.type = course_type  # Set course_type automatically
            
            # Handle paid course validation
            if course_type == 'paid':
                if not student_data.payment_method:
                    form.add_error('payment_method', 'Payment method is required for paid courses.')
                payment_screenshot = request.FILES.get('payment_screenshot')
                if not payment_screenshot:
                    form.add_error('payment_screenshot', 'Payment screenshot is required for paid courses.')
                else:
                    student_data.payment_screenshot = payment_screenshot  # Assign the file to the model field
            
            # Save the student data only if there are no errors
            if not form.errors:
                student_data.save()
                print("Student data saved successfully.")

                # Save subscription details
                subscription = Subscription(
                    user=student_data.user,
                    student=student_data,
                    course_title=course_name,
                    course_type=course_type,

                )
                subscription.save()
                print("Subscription saved successfully.")
                
                return render(request, 'subscribe.html', {'subscription_success': True, 'course_name': course_name})
            else:
                print(f"Form errors: {form.errors}")
        else:
            print(f"Form is invalid: {form.errors}")
    else:
        # Pre-fill form with course name and type
        form = SubscriptionForm(initial={'course_name': course_name, 'type': course_type})

    return render(request, 'subscribe.html', {'form': form, 'course_name': course_name, 'course_type': course_type})

def home(request):
    return render(request,'content.html')

def course_detail(request, course_id):
    # Fetch the course
    course = get_object_or_404(Course, id=course_id)

    # Redirect unauthenticated users
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect unauthenticated users to login

    # Fetch the student's subscription
    subscription = Subscription.objects.filter(
        course_title=course.title,  # Ensure course title matches
        user=request.user           # Match the logged-in user
    ).first()

    # Debug print to verify subscription retrieval
    print("Subscription:", subscription)

    # Fetch course contents if subscribed
    course_contents = course.contents.all() if subscription else []

    # Render course details, passing subscription status
    return render(request, 'course_details.html', {
        'course': course,
        'subscription': subscription,
        'course_contents': course_contents,
    })




