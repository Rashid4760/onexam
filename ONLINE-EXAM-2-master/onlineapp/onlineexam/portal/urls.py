from django.urls import path
from . import views

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('register1/', views.register1, name='register1'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashstudent/', views.dashstudent, name='dashstudent'),
    path('exam/', views.exam, name='exam'),
    path('adminregister/', views.admin_register, name='adminregister'),
    path('studentregister/', views.student_register, name='studentregister'),
    path('loginpage/',views.loginpage,name='loginpage'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('studentlogin/',views.studentlogin,name='studentlogin'),
    path('studentlogout/',views.studentlogout,name='studentlogout'),
    path('question/',views.question,name='question'),
    path('home/',views.home,name='home'),
    #path('start_recognition/',views.start_recognition,name='start_recognition'),
    path('quiz/', views.quiz_view, name='quiz_view'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('release_camera/', views.release_camera, name='release_camera'),
    

   


]