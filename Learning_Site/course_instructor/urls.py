"""
URL configuration for courseselling project.
"""

from django.urls import path
from .views import (
    create_course,
    add_update_content,
    CustomLoginView,
    create_quiz,
    add_questions,
    quiz_view,
    filter_courses,
)

urlpatterns = [
    path("create_course", create_course, name="create_course"),
    path("add_update_content/<int:course_id>/", add_update_content, name="add_update_content"),
    path("registration/login/", CustomLoginView.as_view(), name="login"),
    path("add-questions/<int:quiz_id>/", add_questions, name="add_questions"),
    path("quiz/<int:content_id>/", quiz_view, name="quiz_view"),
    path("create-quiz/<int:video_id>/", create_quiz, name="create_quiz"),
    path("courses/", filter_courses, name="filter_courses"),
]
