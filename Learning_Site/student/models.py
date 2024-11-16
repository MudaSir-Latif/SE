from django.db import models
from django.contrib.auth.models import User

class student(models.Model):
    COURSE_TYPE_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]
    # Make user field optional by using null=True and blank=True
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    subscripted_at = models.DateTimeField(auto_now_add=True)
    course_name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES, default='unpaid')

    def __str__(self):
        return self.full_name
