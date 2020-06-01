# Generated by Django 2.2.5 on 2020-01-01 12:34

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('mobile', models.BigIntegerField(null=True)),
                ('address', models.TextField(default='', max_length=201)),
                ('experience', models.BigIntegerField(null=True)),
                ('dateofreg', models.DateField(default=datetime.date.today)),
                ('is_student', models.BooleanField(default=False, verbose_name='student status')),
                ('is_faculty', models.BooleanField(default=False, verbose_name='faculty status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'User',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('subject', models.TextField(max_length=50)),
                ('coursename', models.TextField(max_length=150)),
                ('duration', models.BigIntegerField(null=True)),
                ('coursestartdate', models.DateField(default=datetime.date.today)),
                ('courseenddate', models.DateField(default=datetime.date.today)),
                ('faculty_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Course',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('questiontext', models.TextField(max_length=150)),
                ('option1', models.TextField(max_length=150)),
                ('option2', models.TextField(max_length=150)),
                ('option3', models.TextField(max_length=150)),
                ('option4', models.TextField(max_length=150)),
                ('correctanswer', models.TextField(max_length=150)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Course')),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourseRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.TextField(max_length=4, null=True)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Course')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'StudentCourseRegistration',
                'unique_together': {('student_id', 'course_id')},
            },
        ),
    ]
