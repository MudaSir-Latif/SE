# Generated by Django 5.1.2 on 2024-11-26 18:07

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('duration', models.DurationField(default=datetime.timedelta(days=30))),
                ('course_type', models.CharField(choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], default='unpaid', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_taught', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issued_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='course_instructor.course')),
            ],
        ),
        migrations.CreateModel(
            name='CourseContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Contenttitle', models.CharField(max_length=255)),
                ('video', models.FileField(max_length=255, upload_to='course_videos/')),
                ('content_type', models.CharField(choices=[('video', 'Video'), ('pdf', 'PDF'), ('text', 'Text')], max_length=100)),
                ('order', models.IntegerField()),
                ('additional_resources', models.FileField(blank=True, null=True, upload_to='resources/')),
                ('is_last_video', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='course_instructor.course')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(editable=False, max_length=255)),
                ('course', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='course_instructor.course')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('option_a', models.CharField(max_length=255)),
                ('option_b', models.CharField(max_length=255)),
                ('option_c', models.CharField(max_length=255)),
                ('option_d', models.CharField(max_length=255)),
                ('correct_answer', models.CharField(choices=[('a', 'Option A'), ('b', 'Option B'), ('c', 'Option C'), ('d', 'Option D')], max_length=1)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='course_instructor.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='QuizAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('passed', models.BooleanField(default=False)),
                ('attempted_at', models.DateTimeField(auto_now_add=True)),
                ('correct_count', models.IntegerField(default=0)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='course_instructor.quiz')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_attempts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VideoWatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watched', models.BooleanField(default=False)),
                ('watched_at', models.DateTimeField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_instructor.coursecontent')),
            ],
            options={
                'unique_together': {('student', 'video_content')},
            },
        ),
    ]
