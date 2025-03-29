from django.contrib import admin
from .models import questionmodel,FaceImage,adminimage,studentimage

# Register your models here.
admin.site.register(questionmodel)
admin.site.register(FaceImage)
admin.site.register(adminimage)
admin.site.register(studentimage)