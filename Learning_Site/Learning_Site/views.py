from django.http import HttpResponse
from django.shortcuts import render
from course_instructor.models import Course


def check(request):
    query=request.GET.get('q','').strip()
    if request.user.profile_main.role=='instrutor':
        courses=Course.objects.filter(instrutor=request.user)
    else:
        courses=Course.objects.all()
    if query:
        courses=courses.filter(title__icontains=query)
    return render(request,'course_list.html',{'courses':courses,'query':query})

