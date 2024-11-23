# authentication/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('creator', 'Creator'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')

    groups = models.ManyToManyField(
        'auth.Group', related_name='custom_user_set', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='custom_user_permissions_set', blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

# Ensure StudentProfile is defined here as well
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Student Profile: {self.user.username}"

# CreatorProfile can also be defined if needed
class CreatorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='creator_profile')
    experience = models.PositiveIntegerField(null=True, blank=True)
    course_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Creator Profile: {self.user.username}"
