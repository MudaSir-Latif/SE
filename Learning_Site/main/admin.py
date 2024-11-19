from django.contrib import admin

# Register your models here.



# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import Profile


# class CourseAdmin(admin.ModelAdmin):
#     pass


class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
# admin.site.register(Enrollment, EnrollmentAdmin)
