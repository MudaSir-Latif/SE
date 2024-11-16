from django.shortcuts import render, redirect
from .models import student

def unpaid_courses(request):
    return render(request, 'content.html')

def paid_courses(request):
    return render(request, 'content.html')


