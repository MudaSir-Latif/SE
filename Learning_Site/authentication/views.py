<<<<<<< HEAD
=======

>>>>>>> 73fa4e4155251e7528ebd7934cf4982ffaed959b
from django.shortcuts import render, redirect
from .form import UserRegistrationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile_main
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist


def select_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')  # Get the selected role
        request.session['user_role'] = role  # Save role in session
        return redirect('authentication:login') # Redirect to the registration form
    
    return render(request, 'select_role.html') 

def register(request):
    role = request.session.get('user_role')  # Retrieve the role from session
    if not role:
       return redirect('authentication:select_role') 
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Create or update profile
            profile, created = Profile_main.objects.get_or_create(user=user)
            #profile.address = form.cleaned_data['address']
            profile.city = form.cleaned_data['city']
            profile.save()

            # login(request, user)
            #return redirect('home')
    else:
        form = UserRegistrationForm()  # Initialize an empty form for GET requests

    return render(request, 'register.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Change 'home' to your desired post-login redirect URL
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

