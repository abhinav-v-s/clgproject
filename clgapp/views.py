from django.shortcuts import render,redirect
from clgapp.models import Course,Student,Usermember
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User,auth
from fnmatch import fnmatchcase
import os


# Create your views here.
def index(request):
    return render(request,'index.html')


def admin_login(request):
    if request.method == "POST":
        username = request.POST['name']
        password = request.POST['password']
        user2 = auth.authenticate(username=username, password=password)
        if user2 is not None:
            if user2.is_staff:
                login(request, user2)
                return redirect('admin_home') 
            else:
                login(request,user2)
                auth.login(request,user2)
                messages.info(request, f'Welcome {username}')
                return redirect('user_home')
        else:
            messages.info(request, "Invalid username or password")
            return redirect('/')
    return render(request, 'index.html')

def admin_home(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, 'admin/admin_home.html')
    return redirect('/')

def admin_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/')
    


def add_course(request):
    if request.user.is_authenticated:
        return render(request, 'admin/add_course.html')
    return redirect('/')

def add_coursedb(request):
    if request.method=="POST":
        course_name=request.POST.get('course_name')
        course_fee=request.POST.get('fee')
        course=Course(course_name=course_name,fee=course_fee)
        course.save()
        return redirect('admin_home')

    
def add_student(request):
    if request.user.is_authenticated:
        courses = Course.objects.all()
        return render(request, 'admin/add_student.html', {'course': courses})
    return redirect('/')

def add_studentdb(request):
    if request.method == "POST":
        student_name = request.POST['name']
        print(student_name)
        student_address = request.POST['address']
        print(student_address)
        age = request.POST['age']
        print(age)

        jdate = request.POST['jdate']
        print(jdate)
        sel = request.POST['sel']
        print(sel)
        course1 = Course.objects.get(id=sel)
        print(course1)
        student = Student(student_name=student_name, student_address=student_address, student_age=age,
                          joining_date=jdate, course=course1)
        student.save()
        return redirect('admin_home')

    
def show_details(request):
    if request.user.is_authenticated:
        student = Student.objects.all()
        return render(request,'admin/show_student.html', {'students': student})
    return redirect('/')




def deletepage(request,pk):
    std=Student.objects.get(id=pk)
    std.delete()
    return redirect('show_details')



def teacher_signup(request):
    courses=Course.objects.all()
    return render(request,'user/signup.html',{'course':courses})

def add_teacherdb(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        email = request.POST.get('email')
        address = request.POST.get('address')
        age = request.POST.get('age')
        number = request.POST.get('number')
        sel = request.POST.get('sel')
        course1 = Course.objects.get(id=sel)
        image = request.FILES.get('file')

        if password == cpassword:
            if User.objects.filter(username=uname).exists():
                messages.info(request, 'This username already exists')
                return redirect('teacher_signup')
            else:
                user = User.objects.create_user(username=uname, first_name=fname, last_name=lname, email=email,password=password)
                user.save()

                member = Usermember(address=address, age=age, number=number, image=image, user=user, course=course1)
                member.save()
                return redirect('/')
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'user/signup.html', {'course': Course.objects.all()})


def show_teacher(request):
    if request.user.is_authenticated:  
        user1 = Usermember.objects.all()
        return render(request, 'admin/show_teacher.html', {'user': user1})
    return redirect('/')
        

def user_home(request):
    if request.user.is_authenticated:
        return render(request,'user/user_home.html')
    return redirect('/')


def edit_page(request,pk):
        student=Student.objects.get(id=pk)
        course=Course.objects.all()
        return render(request,'admin/edit.html',{'students':student,'courses':course})

def edit_details(request, pk):
    if request.method == 'POST':
        student = Student.objects.get(id=pk)
        sel1 = request.POST.get('sel')
        course = Course.objects.get(id=sel1)
        student.student_name = request.POST.get('name')  
        student.student_address = request.POST.get('address')
        student.student_age = request.POST.get('age')
        student.joining_date = request.POST.get('jdate')
        student.course = course  

        student.save()
        return redirect('show_details')
    return render(request, 'admin/edit.html')



def profile(request):
    if request.user.is_authenticated:
        current_user = request.user.id

        try:
            user1 = Usermember.objects.filter(user_id=current_user) 
        except Usermember.DoesNotExist:
            user1 = None  

        return render(request, 'user/profile.html', {'users': user1})


def edit(request, pk):
    if request.user.is_authenticated:
        current_user = request.user.id
        user1 = Usermember.objects.get(user_id=current_user)
        user2 = User.objects.get(id=current_user)

        if request.method == 'POST':
            if 'file' in request.FILES:
                if user1.image:
                    os.remove(user1.image.path)
                user1.image = request.FILES['file']

            user2.first_name = request.POST.get('fname')
            user2.last_name = request.POST.get('lname')
            user2.username = request.POST.get('uname')
            # Use set_password to securely update the password
            password = request.POST.get('password')
            if password:
                user2.set_password(password)

            user2.email = request.POST.get('email')
            user1.age = request.POST.get('age')
            user1.address = request.POST.get('address')
            user1.number = request.POST.get('number')

            user1.save()
            user2.save()
            return redirect('profile')

        return render(request, 'user/user_edit.html', {'user': user1})
    
    return redirect('/')



def delete(request,pk):
    user=Usermember.objects.get(id=pk)
    if user.image:
        user.image.delete()
    user.delete()
    user.user.delete()
    return redirect('show_teacher')