from django.contrib import admin
from .models import User
from .models import Course
from .models import StudentCourseRegistration
from .models import Question
from .models import Lecture



admin.site.register(User)
admin.site.register(Course)
admin.site.register(StudentCourseRegistration)
admin.site.register(Question)
admin.site.register(Lecture)

# Register your models here.
