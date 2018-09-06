# Django-REST-Framework 的应用



#### requirements.txt 文件用于记录项目所使用的 第三方包

```python
Django              1.11.3
django-filter       1.0.4
djangorestframework 3.6.3
Markdown            2.6.8
mysqlclient         1.3.13
Pillow              5.2.0
pip                 18.0
pytz                2018.5
setuptools          40.2.0
wheel               0.31.1
```

### user model 设计:

```python
# user.models.py
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
        return self.name
    

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

```

 **上面的 UserProfile 字段并没有替换掉我们系统中的用户, 想要替换需要在我们的 settings 中添加一个字段:**

```python
# settings.py
# 将User表中的字段替换掉系统中的用户
AUTH_USER_MODEL = 'user.UserProfile'
```

