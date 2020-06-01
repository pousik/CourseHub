from django.contrib import auth
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from datetime import date,datetime
from main.models import Course
from main.models import Lecture
from main.models import StudentCourseRegistration
from main.models import Question




User=get_user_model()

def basic(request):
    return render(request,'basic.html')
@login_required
def exam1(request,courseid):
    all_question=Question.objects.filter(course_id=courseid)
    
    count=0;
    if request.method=="POST":
        for question in all_question:
            id=question.question_id
            choice=request.POST.get(id)
            if choice==question.correctanswer:
                print('yes')
                count=count+1
                 
        print(count)    
       
    
    return render(request,'Exam1.html',{'all_question':all_question,'count':count})

def questionupload(request):
    all_courses = Course.objects.all()
    courses = {}
    for i in range(len(all_courses)):
        courses[i] = all_courses[i]
        
    if request.method=="POST":
        n = int(request.POST['number'])
        titles = request.POST.getlist('title')
        firstoption=request.POST.getlist('option1')
        secondoption=request.POST.getlist('option2')
        thirdoption=request.POST.getlist('option3')
        fourthoption=request.POST.getlist('option4')
        correctanswer=request.POST.getlist('answer')
        selected_item =request.POST.get('itemid')
        for i in range(n):
            question_details = Question()
            question_details.question_id = str(selected_item)+str(i)
            question_details.questiontext=titles[i]
            question_details.course_id = Course.objects.get(course_id = selected_item)
            question_details.option1 = firstoption[i]
            question_details.option2 = secondoption[i]
            question_details.option3 = thirdoption[i]
            question_details.option4 = fourthoption[i]
            question_details.correctanswer =correctanswer[i]
            question_details.save()
        return render(request,'test.html')
        
        
    
    return render(request, 'questionupload.html', {'courses': courses })

    

@login_required
def profile(request,username):
    
    student=None
    all_student=User.objects.filter(username=str(username))
    if len(all_student) > 0:
        student = all_student[0]
    else:
        student = None
    return render(request, 'profile.html', {'student': student })
    '''
    student=None
    all_student=User.objects.all()
    students={}
    for i in range(len(all_student)):
        students[i]=all_student[i]
        
    student=students[int(username)]
    
    return render(request, 'profile.html', {'student': student })
    
    '''

@login_required
def coursesingle(request,courseid):
    
    cour = None
    all_courses = Course.objects.all()
    courses = {}
    
    for i in range(len(all_courses)):
        courses[i] = all_courses[i]
        
    
    cour = courses[int(courseid)]
    
    '''
    cour=None
    course_list=Course.objects.filter(course_id=str(courseid.course_id))
    if len(course_list) > 0:
        cour = course_list[0]
    else:
        cour = None
    '''
    if request.method=="POST":
        scoureg=StudentCourseRegistration()
        scoureg.student_id=request.user
        scoureg.course_id=cour
        scoureg.save()
        return redirect('home')
    
    # return the emp_detail.html template file to client, and pass the filtered out Employee object.
    return render(request, 'coursesingle.html', {'cour': cour , 'key' : courseid })

    
 
    

    
def logout(request):
    auth.logout(request)
    return redirect('home')
@login_required
def mycourses(request,username):
    all_student = StudentCourseRegistration.objects.filter(student_id=username)
    
    
            
    
    return render(request, 'mycourses.html', {'all_student':all_student,'key' : username })
    
    
def courses(request):
    all_courses = Course.objects.all()
    courses = {}
    for i in range(len(all_courses)):
        courses[i] = all_courses[i]
    return render(request, 'courses.html', {'courses': courses })


def videotest(request):
    lecture = Lecture.objects.all()
    return render(request, 'videotest.html', {'videofile': lecture.lecturevideo})

@login_required
def test(request):
    all_courses = Course.objects.all()
    courses = {}
    for i in range(len(all_courses)):
        courses[i] = all_courses[i]
    return render(request, 'test.html', {'courses': courses })
    

def home(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username= request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request, user)
            if user.is_faculty:
                return redirect('courseregistration')
            else:
                return redirect('home')
        else:
            return render(request, 'login.html', {'error' : 'Wrong Username or Password !'})
    
    return render(request, 'login.html')


def s_registration(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password2']:
            try:
                user = User.objects.get(username = request.POST['username'])
                return render(request, 'register.html' , {'error' : 'Username already taken !!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],password = request.POST['password'],
                                                first_name = request.POST['firstname'], last_name=request.POST['lastname'], 
                                                address =  request.POST['address'], email = request.POST['email'],
                                                mobile= request.POST['mobile'],is_student=True)
                auth.login(request, user)
                return redirect('s_registration')
        else:
            return render(request, 'register.html' , {'error' : 'Password dis not Match !!'})
        
    else:
       return render(request,'register.html')

# Create your views here.
def f_registration(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password2']:
            try:
                user = User.objects.get(username = request.POST['username'])
                return render(request, 'facultyregister.html' , {'error' : 'Username already taken !!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],password = request.POST['password'],
                                                first_name = request.POST['firstname'], last_name=request.POST['lastname'],
                                                experience=request.POST['experience'],
                                                address =  request.POST['address'], email = request.POST['email'],
                                                mobile= request.POST['mobile'],is_faculty=True)
                auth.login(request, user)
                return redirect('f_registration')
        else:
            return render(request, 'facultyregister.html' , {'error' : 'Password dis not Match !!'})
        
    else:
       return render(request,'facultyregister.html')

@login_required
def courseregistration(request):
    if request.method == "POST":
        course_details = Course()
        course_details.subject = request.POST['catagory']
        course_details.coursename = request.POST['coursename']
        course_details.description=request.POST['description']
        course_details.image=request.FILES['image']
        course_details.coursestartdate = request.POST['startdate']
        course_details.courseenddate = request.POST['enddate']
        course_details.duration = request.POST['duration']
        course_details.course_id =request.POST['coursename']
        course_details.faculty_id = request.user
        course_details.save()
        
        '''for f in request.FILES.get('videopath'):
            print("hello")
            print(f)'''
            
        n = int(request.POST['number'])
        titles = request.POST.getlist('title')
        videos = request.FILES.getlist('videopath')
        for i in range(n):
            lecture_details = Lecture()
            lecture_details.lecture_id = str(request.POST['coursename'])+str(i)
            lecture_details.course_id =Course.objects.last()
            lecture_details.lecturedate = date.today()
            lecture_details.lecturename = titles[i]
            lecture_details.lecturevideo = videos[i]
            lecture_details.save()
        
        return redirect('test')
        
    else:
        return render(request, 'courseregistration.html')




def allvideos(request,courseid):
    all_courses=Course.objects.filter(course_id=courseid)
    all_videos=Lecture.objects.filter(course_id=courseid)
    return render(request, 'allvideos.html', {'all_videos':all_videos,'key' : courseid,'all_courses':all_courses})
    '''
    video = None
    all_videos = Lecture.objects.all()
    videos = {}
    
    for i in range(len(all_videos)):
        videos[i] = all_videos[i]
        
    
    video = videos[int(courseid)]
    
    
    return render(request, 'allvideos.html', {'video': video , 'key' : courseid })

    '''
    









