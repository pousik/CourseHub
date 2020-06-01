from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date



class User(AbstractUser):
    mobile=models.BigIntegerField(null=True)
    address=models.TextField(max_length=201,default='')
    experience=models.BigIntegerField(null=True)
    dateofreg=models.DateField(default=date.today)
    is_student=models.BooleanField('student status',default=False)
    is_faculty=models.BooleanField('faculty status',default=False)
    class Meta:
        db_table='User'
        
class Course(models.Model):
    course_id=models.CharField(max_length=100,primary_key=True)
    subject=models.TextField(max_length=50)
    coursename=models.TextField(max_length=150)
    image=models.ImageField(upload_to='images/',null=True)
    description=models.TextField(max_length=300,default='',null=True)
    duration=models.BigIntegerField(null=True)
    coursestartdate=models.DateField(default=date.today)
    courseenddate=models.DateField(default=date.today)
    faculty_id=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table='Course'
        
        
class StudentCourseRegistration(models.Model):
    result = models.TextField(max_length=4,null = True)
    student_id = models.ForeignKey(User, on_delete = models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete = models.CASCADE)
    class Meta:
        db_table = 'StudentCourseRegistration'
        unique_together = (('student_id','course_id'),)
        
class   Question(models.Model):
    question_id=models.CharField(max_length=20,primary_key=True)
    questiontext=models.TextField(max_length=150)
    option1=models.TextField(max_length=150)
    option2=models.TextField(max_length=150)
    option3=models.TextField(max_length=150)
    option4=models.TextField(max_length=150)
    correctanswer=models.TextField(max_length=150)
    course_id=models.ForeignKey(Course, on_delete=models.CASCADE)
    class Meta:
        db_table='Question'
        
class Lecture(models.Model):
    lecture_id=models.CharField(max_length=100,primary_key=True)
    lecturename=models.TextField(max_length=200)
    lecturedate=models.DateField(default=date.today)
    lecturevideo=models.FileField(upload_to='videos/')
    course_id=models.ForeignKey(Course, on_delete=models.CASCADE)
    class Meta:
        db_table='Lecture'
    

