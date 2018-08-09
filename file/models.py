from django.db import models

# Create your models here.
#建立文件名表
class Filename(models.Model):
    name = models.CharField(max_length=60,null=False,unique=True)
    classify = models.CharField(max_length=120,null=False,default="null")
    time = models.CharField(max_length=60,null=False,default="null")