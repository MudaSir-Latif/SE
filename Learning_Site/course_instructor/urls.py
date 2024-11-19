"""
URL configuration for courseselling project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import create_course,add_update_content,CustomLoginView,create_quiz,add_questions,quiz_view,mark_video_watched


urlpatterns = [
    path("create_course",create_course,name='create_course'),
    path("add_update_content/<int:course_id>/",add_update_content,name='add_update_content'),
    path('registration/login/', CustomLoginView.as_view(), name='login'),
    # path('mark-video-watched/', mark_video_watched, name='mark_video_watched'),
    # path('create-quiz', create_quiz, name='create_quiz'),
    path('add-questions/<int:quiz_id>/',add_questions, name='add_questions'),
    path('quiz/<int:content_id>/',quiz_view, name='quiz_view'),
    path('create-quiz/<int:video_id>/',create_quiz, name='create_quiz'),
    # path('mark-video-watched/', mark_video_watched, name='mark_video_watched'),
    
]


