from django.contrib import admin
from django.urls import path,include
from .views import if_is_instructor,main_page,course_detail
from django.contrib.auth import views as auth_views
from course_instructor.views import mark_video_watched
from .views import your_view


urlpatterns = [
    path("",if_is_instructor,name='main'),
    path("main_page",main_page,name='main'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('registration/login/', auth_views.LoginView.as_view(), name='login'),
    path('mark-video-watched/', mark_video_watched, name='mark_video_watched'),
     path('your-view/', your_view, name='your_view'),
    
]
