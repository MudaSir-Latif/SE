from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
app_name = 'authentication'
urlpatterns = [
    path('learner-register',views.register, name='register'),
    path('select-role/', views.select_role, name='select_role'),  # Role selection page
    path('login/', views.login_view, name='login'),

]

