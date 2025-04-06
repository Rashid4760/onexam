from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, 'index.html')

def studentloginForm(request):
    return render(request, 'studentlogin.html')

def teacherloginForm(request):
    return render(request, 'teaherlogin.html')

def registerForm(request):
    return render(request, 'register.html')

def studentregistration(request):
    if request.method == 'POST':
        sfname=request.POST['sfirst']
        slname=request.POST['slast']
        smail = request.POST['semail']
        suname = request.POST['susername']   
        spass = request.POST['spassword']   
        scon = request.POST['scpassword']
        ssdept = request.POST['sdept']       
        if spass == scon:
            user = User.objects.create_user(username=suname, password=spass, first_name=sfname, last_name=slname, email=smail)
            user.save()
            student = Student.objects.create(user=user,depts=ssdept)
            student.save()
            return redirect(index)
        else:
            return redirect(registerForm)
        
        return redirect('index')  
    return redirect(index)

def teacherregistration(request):
    if request.method == 'POST':
        tfname=request.POST['tfirst']
        tlname=request.POST['tlast']
        tmail = request.POST['temail']
        tuname = request.POST['tusername']   
        tpass = request.POST['tpassword']   
        tcon = request.POST['tcpassword']
        ttdept = request.POST['tdept']       
        if tpass == tcon:
            user = User.objects.create_user(username=tuname, password=tpass, first_name=tfname, last_name=tlname, email=tmail)
            user.save()
            teacher = Teacher.objects.create(user=user,dept=ttdept)
            teacher.save()
            return redirect(index)
        else:
            return redirect(registerForm)

def stddash(request):
    if request.user.is_authenticated:
        student = Student.objects.get(user=request.user)
        context={
            'student': student,
        }
     
    return render(request, 'studentdash.html',context=context)

def studentlogin(request):
    if request.method == 'POST':
        suname = request.POST.get('susername')
        spass = request.POST.get('spassword')
        
        if suname and spass:  # Ensure both username and password are provided
            user = authenticate(username=suname, password=spass)
            if user is not None:
                login(request, user)
                return redirect(stddash)
            else:
                return redirect(studentloginForm)
        else:
            return redirect(studentloginForm)  # Redirect if fields are empty
    return redirect(index)

def imageUpload(request):
    if request.method == 'POST':
        image = request.FILES['image']
        student = Student.objects.get(user=request.user)
        student.image = image
        student.save()
        return redirect(stddash)
    return redirect(stddash)    

def logoutUser(request):
    logout(request)
    return redirect(index)

def teacherdash(request):
        teacher = Teacher.objects.get(user=request.user)
        context={
            'teacher': teacher,
        }
     
        return render(request, 'teachdash.html',context=context)
def teacherlogin(request):  
    if request.method == 'POST':
        tuname = request.POST.get('tusername')
        tpass = request.POST.get('tpassword')
        
        if tuname and tpass:  # Ensure both username and password are provided
            user = authenticate(username=tuname, password=tpass)
            if user is not None:
                login(request, user)
                return redirect(teacherdash)
            else:
                return redirect(teacherloginForm)
        else:
            return redirect(teacherloginForm)  # Redirect if fields are empty
    return redirect(index)

def viewexam(request):
    return render(request, 'viewexam.html')

def create_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct_option = request.POST.get('correct_option')

        # Save the question to the database
        Question.objects.create(
            question_text=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option
             )
        return redirect(teacherdash)  # Redirect back to the teacher dashboard
    return HttpResponse("Invalid request method", status=405)