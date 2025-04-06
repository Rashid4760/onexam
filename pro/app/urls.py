from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('studentlogin', views.studentloginForm, name='studentlogin'),
    path('teacherlogin', views.teacherloginForm, name='teacherlogin'),
    path('register', views.registerForm, name='register'),
    path('studentregistration', views.studentregistration, name='studentregistration'),
    path('teacherregistration', views.teacherregistration, name='teacherregistration'),
    path('stddash', views.stddash, name='stddash'),
    path('studentlogindash', views.studentlogin, name='studentlogindash'),
    path('images', views.imageUpload, name='images'),
    path('slogout', views.logoutUser, name='slogout'),
    path('tlogindash', views.teacherlogin, name='tlogindash'),
    path('tdash',views.teacherdash, name='tdash'),
    path('exam',views.viewexam, name='exam'),
     path('create-question', views.create_question, name='create_question'),

]
