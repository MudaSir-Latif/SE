from django.urls import path
from . import views

urlpatterns = [
    path('unpaid-courses/', views.unpaid_courses, name='unpaid_courses'),
    path('paid-courses/', views.paid_courses, name='paid_courses'),
]
