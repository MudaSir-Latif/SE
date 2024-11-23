from django.contrib import admin

# Register your models here.


# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import Course,CourseContent
from django.contrib import admin
from .models import Quiz, Question,VideoWatch


class CourseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Course, CourseAdmin)

class CourseContentAdmin(admin.ModelAdmin):
    pass
admin.site.register(CourseContent, CourseContentAdmin)
# class EnrollmentAdmin(admin.ModelAdmin):
#     pass

# admin.site.register(Enrollment, EnrollmentAdmin)



from .models import Purchase
class PurchaseAdmin(admin.ModelAdmin):
    pass


# class LocationAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Purchase,PurchaseAdmin)



class QuizAdmin(admin.ModelAdmin):
    pass

admin.site.register(Quiz,QuizAdmin)

class QuestionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Question,QuestionAdmin)

class VideoWatchAdmin(admin.ModelAdmin):
    pass

admin.site.register(VideoWatch,VideoWatchAdmin)

# class QuestionInline(admin.TabularInline):  # Or you can use StackedInline
#     model = Question
#     extra = 1  # This sets the number of extra empty forms displayed

# class QuizAdmin(admin.ModelAdmin):
#     inlines = [QuestionInline]

# admin.site.register(Quiz, QuizAdmin)





# class QuizAttemptAdmin(admin.ModelAdmin):
#     pass

# admin.site.register(QuizAttempt,QuizAttemptAdmin)


# class QuizAccessAdmin(admin.ModelAdmin):
#     pass

# admin.site.register(QuizAccess,QuizAccessAdmin)



# class NextVideoAccessAdmin(admin.ModelAdmin):
#     pass

# admin.site.register(NextVideoAccess,NextVideoAccessAdmin)