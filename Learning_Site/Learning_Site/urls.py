"""
URL configuration for Learning_Site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from course_instructor import urls as course_instructor_urls
from authentication import urls
from main import urls as main_app_urls
from django.contrib.auth.views import LoginView
from course_instructor.views import CustomLoginView  # Import the custom login view

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
=======
    path('main/', views.main),
    path('student/',include('student.urls')),
    path('',include(main_app_urls)),
>>>>>>> 73fa4e4155251e7528ebd7934cf4982ffaed959b
    path('',include(course_instructor_urls)),
    path('student/',include('student.urls')),
    path('authentication/',include('authentication.urls')),
    path('',include('main.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:  # Serve media files only during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)