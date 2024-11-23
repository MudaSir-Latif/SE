from django.contrib import admin
<<<<<<< HEAD
from .models import Profile_main

admin.site.register(Profile_main)
=======
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, CreatorProfile

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type',)}),
    )

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age']

@admin.register(CreatorProfile)
class CreatorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'experience', 'course_type']
>>>>>>> 3ebd0bd694fbce12bbd0ab089bba42c4a3d99d51
