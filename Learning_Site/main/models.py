from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # Linking Profile to Django's built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Common fields for all users
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Distinguishing whether the user is a student, an instructor, or both
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    
    # Additional information for course instructors
    instructor_bio = models.TextField(blank=True, null=True)
    expertise = models.CharField(max_length=255, blank=True, null=True)
    
    # Timestamp for tracking when the profile was created and updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def is_student_only(self):
        return self.is_student and not self.is_instructor

    def is_instructor_only(self):
        return self.is_instructor and not self.is_student

    def is_both(self):
        return self.is_student and self.is_instructor
