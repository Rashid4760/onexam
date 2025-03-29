from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class questionmodel(models.Model):
    question_number=models.IntegerField(blank=True,null=True,default=1)
    question=models.CharField(max_length=500)
    answer1=models.CharField(max_length=200)
    answer2=models.CharField(max_length=200)
    answer3=models.CharField(max_length=200)
    answer4=models.CharField(max_length=200)
    rightanswer=models.CharField(max_length=200)

    def __str__(self):
        return f"Q{self.question_number}: {self.question}"
  

class adminimage(models.Model):

    teacher=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='adminimage/')
    confirmadmin=models.BooleanField(default=False,blank=True)

    def __str__(self):
        return f"{self.teacher.username}"



class studentimage(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    image=models.ImageField(upload_to='studentimage/')
    confirmstudent=models.BooleanField(default=False,blank=True)

    def __str__(self):
        return f"{self.student.username}"


class FaceImage(models.Model):
    image = models.ImageField(upload_to='face_images/')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

