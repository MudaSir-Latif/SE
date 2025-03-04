# Generated by Django 5.1.2 on 2025-02-05 10:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_instructor', '0005_course_price'),
        ('student', '0002_alter_student_user_alter_subscription_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='course_title',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='course_type',
        ),
        migrations.AddField(
            model_name='subscription',
            name='course',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='course_instructor.course'),
            preserve_default=False,
        ),
    ]
