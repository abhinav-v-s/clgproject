from django.contrib import admin
from clgapp.models import Course
from clgapp.models import Student
from clgapp.models import Usermember

# Register your models here.

admin.site.register(Course)

admin.site.register(Student)

admin.site.register(Usermember)

