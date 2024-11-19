from django.shortcuts import render, redirect
from .models import student
from .forms import SubscriptionForm

def unpaid_courses(request):
    return render(request, 'content.html')

def paid_courses(request):
    return render(request, 'content.html')

def subscribe(request, course_name, course_type):
    print(f"Course Name: {course_name}, Course Type: {course_type}")  # Debugging line
    
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid, saving...")  # Debugging linem
            subscription = form.save(commit=False)
            subscription.course_name = course_name  # Set course_name automatically
            subscription.type = course_type  # Set course_type automatically
            
            # If the user is logged in, assign the current user to the student record
            # if request.user.is_authenticated:
            #      subscription.user = request.user
            if course_type == 'paid':
                if not subscription.payment_method:
                    form.add_error('payment_method', 'Payment method is required for paid courses.')
                payment_screenshot = request.FILES.get('payment_screenshot')
                if not payment_screenshot:
                    form.add_error('payment_screenshot', 'Payment screenshot is required for paid courses.')
                else:
                    subscription.payment_screenshot = payment_screenshot  # Assign the file to the model field
            # Save the subscription only if there are no errors
            if not form.errors:
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




