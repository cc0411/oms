from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    mobile = models.CharField(max_length=11,verbose_name=u'手机号',default='')
    image = models.ImageField(max_length=100,verbose_name=u'头像',upload_to='image/%Y/%m',default='image/default.png')
    name = models.CharField(max_length=32,verbose_name=u'姓名',default='')
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name
