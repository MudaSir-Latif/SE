from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta
from main.models import Profile

class Course(models.Model):
    COURSE_TYPE_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.DurationField(default=timedelta(days=30))
    instructor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='courses_taught')
    course_type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES, default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

class CourseContent(models.Model):
    course = models.ForeignKey(Course, related_name='contents', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='course_videos/', max_length=255)
    content_type = models.CharField(max_length=100, choices=[('video', 'Video'), ('pdf', 'PDF'), ('text', 'Text')])
    order = models.IntegerField()
    additional_resources = models.FileField(upload_to='resources/', null=True, blank=True)
    is_first_video = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.content_type})"

    def save(self, *args, **kwargs):
        if self.is_first_video:
            CourseContent.objects.filter(course=self.course, is_first_video=True).update(is_first_video=False)
        super(CourseContent, self).save(*args, **kwargs)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class Purchase(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='purchased_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='purchases')
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} bought {self.course.title}"

    class Meta:
        unique_together = ('student', 'course')

class Quiz(models.Model):
    course_content = models.OneToOneField(CourseContent, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

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
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    video_content = models.ForeignKey(CourseContent, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    watched_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['student', 'video_content']

    def __str__(self):
        return f'{self.student.username} watched {self.video_content.title}'
