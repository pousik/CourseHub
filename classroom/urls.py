"""classroom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('basic/',views.basic,name='basic'),
    
    
    path('experiment/',views.experiment,name='experiment'),
     path('confirmregistration/',views.confirmregistration,name='confirmregistration'),
     path('generatecertificate/',views.generatecertificate,name='generatecertificate'),
    
    path('login/',views.login,name='login'),
    path('test/',views.test,name='test'),
    path('videotest/',views.videotest,name='videotest'),
    path('studentregistration/',views.s_registration,name='s_registration'),
    path('facultyregistration/',views.f_registration,name='f_registration'),
    path('courseregistration/',views.courseregistration,name='courseregistration'),

    path('logout/',views.logout,name='logout'),
    path('courses/',views.courses,name='courses'),
    path(r'^allvideos/(?P<courseid>\w+)/$', views.allvideos, name='allvideos'),
    path(r'^mycourses/(?P<username>\w+)/$', views.mycourses, name='mycourses'),

    path(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    
    path(r'^coursesingle/(?P<courseid>\w+)/$', views.coursesingle, name='coursesingle'),
    path('questionupload/',views.questionupload,name='questionupload'),
    path(r'^exam1/(?P<courseid>\w+)/$', views.exam1, name='exam1'),
     path(r'^invoice/(?P<courseid>\w+)/$', views.getPdfPage, name='invoice'),
    
    
   
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
