from django.contrib import auth
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.shortcuts import render_to_response
from datetime import date,datetime
from main.models import Course
from main.models import Lecture
from main.models import StudentCourseRegistration
from main.models import Question
from main.models import Examination


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from django.views.generic import View







User=get_user_model()



def facultyprofile(request):
    faculty=User.objects.filter(username=request.user)
    
    
    return render(request, 'facultyprofile.html',{'faculty':faculty})
    

def questionconfirmation(request):
    return render(request,'questionconfirmation.html')

def addcourseconfirmation(request):
    return render(request,'addingcourseconfirmation.html')

def generatecertificate(request):
    all_courses=Examination.objects.filter(student_id=request.user)
    
    
    
        
        
    return render(request,'generatecertificate.html',{'all_courses':all_courses})


def getPdfPage(request,courseid):
    all_student=Examination.objects.filter(examination_id=courseid)
    data={'students':all_student}
    template=get_template("certificate.html")
    data_p=template.render(data)
    response=BytesIO()

    pdfPage=pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")),response)
    if not pdfPage.err:
        return HttpResponse(response.getvalue(),content_type="application/pdf")
    else:
        return HttpResponse("Error Generating PDF")
    
    
def basic(request):
    return render(request,'basic.html')

def confirmregistration(request):
    return render(request,'confirmregistration.html')

def experiment(request):
    return render(request,'experiment.html')

@login_required
def exam1(request,courseid):
    all_question=Question.objects.filter(course_id=courseid)
    value=len(all_question)
      
    exam_details=Examination()
    count=0;
    if request.method=="POST":
        try:
            for question in all_question:
                id=question.question_id
                choice=request.POST.get(id)
                print(choice)
                print(question.correctanswer)
                if choice==question.correctanswer:
                    count=count+1
                    print(count)
                    
                    
            print(count)    
            aggregate=float(count/value)*100
            print(aggregate)
            if aggregate > 40:
               exam_details.resultstatus="pass"
            else:
               exam_details.resultstatus="fail"
            exam_details.student_id=request.user
            exam_details.course_id=Course.objects.get(course_id=courseid)
            exam_details.aggregate=aggregate
            exam_details.completiondate=date.today()
            
            exam_details.save()
            examdone=True
            return render(request,'Exam1.html',{'all_question':all_question,'aggregate':aggregate,'value':value,'examdone':examdone})
        except IntegrityError:
            
            return render(request, 'Exam1.html' , {'error' : 'Username already given exam !!'})
        
        
        
    
    return render(request,'Exam1.html',{'all_question':all_question,'count':count,'value':value})

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
        return render(request,'questionconfirmation.html')
        
        
    
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
        try:         
            scoureg=StudentCourseRegistration()
            scoureg.student_id=request.user
            scoureg.course_id=cour
            scoureg.save()
            return render(request,'confirmregistration.html')
        except IntegrityError:
            return render(request, 'coursesingle.html' , {'error' : 'You have already register for this Course !!','cour': cour , 'key' : courseid})
            
            
    else:
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
                return redirect('facultyprofile')
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
                return render(request,'login.html')
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
                return render(request,'login.html')
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
        
        return redirect(request,'addingcourseconfirmation.html')
        
    else:
        return render(request, 'courseregistration.html')




def allvideos(request,courseid):
    all_courses=Course.objects.filter(course_id=courseid)
    all_videos=Lecture.objects.filter(course_id=courseid)
    getcourses=Question.objects.filter(course_id=courseid)
    courselen=len(getcourses)
    '''try:
        status=Question.objects.get(course_id=courseid)
    except Question.DoesNotExists:
        status=None
       ''' 
    return render(request, 'allvideos.html', {'all_videos':all_videos,'key' : courseid,'all_courses':all_courses,'courselen':courselen})
    
    '''
    video = None
    all_videos = Lecture.objects.all()
    videos = {}
    
    for i in range(len(all_videos)):
        videos[i] = all_videos[i]
        
    
    video = videos[int(courseid)]
    
    
    return render(request, 'allvideos.html', {'video': video , 'key' : courseid })

    '''
    










