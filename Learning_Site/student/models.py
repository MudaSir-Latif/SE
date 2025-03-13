from django.db import models
from django.contrib.auth.models import User
from course_instructor.models import Course

class Student(models.Model):
    COURSE_TYPE_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]

    PAYMENT_METHOD_CHOICES = [
    ('credit_card', 'Credit Card'),
    ('paypal', 'PayPal'),
    ('bank_transfer', 'Bank Transfer'),
]
    
    # Make user field optional by using null=True and blank=True
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    subscripted_at = models.DateTimeField(auto_now_add=True)
    course_name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES, default='unpaid')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', null=True, blank=True)  


    def __str__(self):
        return self.full_name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='subscriptions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.student.full_name} - {self.course.title}"

    def has_access(self):
        # Unpaid courses are open; paid courses need a payment method
        return self.course.course_type == 'unpaid' or self.student.payment_method is not None