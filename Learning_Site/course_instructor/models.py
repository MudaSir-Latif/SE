from django.db import models

# Create your models here.


# Create your models here.

from django.contrib.auth.models import User

# from course_details.models import Course,CourseContent
from django.core.exceptions import ValidationError
from main.models import Profile


from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings  # To reference User and Profile models
from datetime import timedelta
from main.models import Profile  # Assuming Profile is in an app named 'users'

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.DurationField(default=timedelta(days=30))  # Duration of the course
    instructor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='courses_taught')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class CourseContent(models.Model):
    course = models.ForeignKey(Course, related_name='contents', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='course_videos/',max_length=255)  # Path to store video files
    content_type = models.CharField(max_length=100, choices=[('video', 'Video'), ('pdf', 'PDF'), ('text', 'Text')])
    order = models.IntegerField()  # To display content in sequence/order
    additional_resources = models.FileField(upload_to='resources/', null=True, blank=True)  # Optional resources
    is_first_video = models.BooleanField(default=False)  # Indicates if this is the first video in the course

    def __str__(self):
        return f"{self.title} ({self.content_type})"    
    
    def save(self, *args, **kwargs):
        # Ensure only one 'is_first_video' is set to True for a course
        if self.is_first_video:
            # Reset other contents for this course to not be the first video
            CourseContent.objects.filter(course=self.course, is_first_video=True).update(is_first_video=False)
        super(CourseContent, self).save(*args, **kwargs)



class Purchase(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='purchased_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='purchases')
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} bought {self.course.title}"
    
    class Meta:
        unique_together = ('student', 'course')  # Ensure a user can buy a course only once


# class VideoProgress(models.Model):
#     student = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     video = models.ForeignKey(CourseContent, on_delete=models.CASCADE)
#     watched = models.BooleanField(default=False)

class Quiz(models.Model):
    course_content = models.OneToOneField(CourseContent, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    # def clean(self):
    #     """
    #     Validate that a quiz contains exactly 10 questions.
    #     """
    #     if self.questions.count() > 10:
    #         raise ValidationError("A quiz can only have a maximum of 10 questions.")

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[
        ('a', 'Option A'),
        ('b', 'Option B'),
        ('c', 'Option C'),
        ('d', 'Option D'),
    ])

    def __str__(self):
        return f"{self.quiz.title} - Question: {self.question_text[:50]}"  
    

class VideoWatch(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Assumes user is the student
    video_content = models.ForeignKey(CourseContent, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    watched_at = models.DateTimeField(null=True, blank=True)  # When the video was marked as watched

    class Meta:
        unique_together = ['student', 'video_content']  # Ensures a student can only watch a video once

    def __str__(self):
        return f'{self.student.username} watched {self.video_content.title}'


# class QuizAttempt(models.Model):
#     student = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
#     score = models.IntegerField()
#     passed = models.BooleanField(default=False)

# class QuizAccess(models.Model):
#     student = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     video = models.ForeignKey(CourseContent, on_delete=models.CASCADE)
#     can_take_quiz = models.BooleanField(default=False)

# class NextVideoAccess(models.Model):
#     student = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     current_video = models.ForeignKey(CourseContent, related_name='current_video', on_delete=models.CASCADE)
#     next_video = models.ForeignKey(CourseContent, related_name='next_video', on_delete=models.CASCADE)
#     can_access = models.BooleanField(default=False)
