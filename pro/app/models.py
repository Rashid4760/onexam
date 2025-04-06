from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dept = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    image = models.ImageField(upload_to='images/')
    depts = models.CharField(max_length=100,blank=True)    

    def __str__(self):
        return self.user.username    

class Question(models.Model):
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1)  # Store '1', '2', '3', or '4'

    def __str__(self):
        return self.question_text