# Learning Site

## Overview

Learning Site is a Django-based web application for online course management. It supports multiple user roles (learners, instructors, admins), course creation, subscription management, quizzes, and payment tracking. The project is structured for easy deployment and extensibility.

## Features

- User authentication and role management (learner, instructor, admin)
- Instructor dashboard for course creation and content management
- Learner dashboard for course subscription and progress tracking
- Course types: Paid and Unpaid
- Payment screenshot upload for paid courses
- Quiz and feedback system for courses
- Media and static file handling
- Admin interface for site management
- Responsive UI with Bootstrap

## Project Structure

```
Learning_Site/
├── authentication/         # User authentication and profile management
├── course_instructor/      # Course and content management for instructors
├── main/                   # Main app for landing and general pages
├── student/                # Student/learner management and subscriptions
├── template/               # HTML templates for all pages
├── static/                 # Static files (CSS, images, etc.)
├── media/                  # Uploaded media (videos, payment screenshots)
├── Learning_Site/          # Project settings and URLs
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel deployment config
└── manage.py               # Django management script
```

## Setup Instructions

1. **Clone the repository:**
	```sh
	git clone <repo-url>
	cd Learning_Site
	```

2. **Create a virtual environment and activate it:**
	```sh
	python -m venv venv
	venv\Scripts\activate  # On Windows
	# source venv/bin/activate  # On macOS/Linux
	```

3. **Install dependencies:**
	```sh
	pip install -r requirements.txt
	```

4. **Apply migrations:**
	```sh
	python manage.py migrate
	```

5. **Create a superuser (admin):**
	```sh
	python manage.py createsuperuser
	```

6. **Run the development server:**
	```sh
	python manage.py runserver
	```

7. **Access the site:**
	- Main site: http://127.0.0.1:8000/
	- Admin: http://127.0.0.1:8000/admin/

## Deployment

- The project includes a `vercel.json` for deployment on Vercel using Python 3.9 and the WSGI entrypoint.
- Configure environment variables and static/media file storage as needed for production.

## Key Apps and Models

- **authentication**: `Profile_main` model for user roles and profile info.
- **course_instructor**: `Course`, `CourseContent`, `Quiz` models for course management.
- **student**: `Student`, `Subscription` models for learner management.

## Media & Static Files

- Media files (uploads) are stored in `media/` and served at `/media/`.
- Static files are in `static/` and served at `/static/`.

## Customization

- Templates are in the `template/` directory and can be customized for branding or UI changes.
- Add new apps or extend models as needed for additional features.

## License

This project is for educational purposes. Please check with the repository owner for licensing details.