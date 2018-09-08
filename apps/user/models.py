from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户:
    AbstractUser: UserProfile并没有替换掉我们系统的拥护
    如果想要替换需要settings中设置
    """
    name = models.CharField(max_length=20, null=True, blank=True, verbose_name='姓名')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", '女')), default='男', verbose_name='性别')
    mobile = models.CharField(max_length=11, verbose_name='电话')
    email = models.CharField(max_length=100, null=True, blank=True,  verbose_name='邮箱')
    
    # null=Ture: 数据库可以为空, blank=True 可以为空
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        
    def __str__(self):
        # return self.name
        return self.username

class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='联系方式')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    # default=datetime.now 不同与 default=datetime.now()
    # 后者为创建表的时间, 前者为点击触动该字段的时候创建时间
    
    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = '短信验证码'
        
    def __str__(self):
        return self.code
