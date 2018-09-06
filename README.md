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



### goods models 设计:

```python
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField


class GoodsCategory(models.Model):
    """
    商品类别:
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目")
    )
    name = models.CharField(default='', max_length=30, verbose_name='类别名称', help_text='类别名称')
    code = models.CharField(default='', max_length=20, verbose_name='类别code', help_text='类别code')
    desc = models.CharField(default='', max_length=20, verbose_name='类别描述', help_text='类别描述')
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name='类别级别', help_text='类别级别')
    category_image = models.CharField("self", null=True, blank=True,  max_length=20, verbose_name='父类级别', related_name='sub_cat')
    # 自关联, 自己指向自己的表
    is_tab = models.BooleanField(default=False, verbose_name='是否导航', help_text='是否导航')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name


class GoodsCategoryBrand(models.Model):
    """
    品牌名:
    """
    name = models.CharField(default="", max_length=30, verbose_name='品牌名', help_text='品牌名')
    desc = models.TextField(default="", max_length=200, verbose_name='品牌描述', help_text='品牌描述')
    image = models.ImageField(upload_to='brand/images/', verbose_name='上传图片')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "品牌"
        verbose_name_plural = verbose_name
        
        
class Goods(models.Model):
    """
    商品
    """
    category = models.ForeignKey(GoodsCategory, null=True, blank=True,  verbose_name='商品类目', help_text='商品类别')
    goods_sn = models.CharField(max_length=50, default="", verbose_name='商品唯一货号')
    name = models.CharField(max_length=300, verbose_name='商品名')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    sold_num = models.IntegerField(default=0, verbose_name='商品销售量')
    fav_num = models.IntegerField(default=0, verbose_name='收藏数')
    goods_num = models.IntegerField(default=0, verbose_name='库存数')
    market_price = models.FloatField(default=0, verbose_name='市场价格')
    shop_price = models.FloatField(default=0, verbose_name='本店价格')
    goods_brief = models.TextField(verbose_name='商品简短描述')
    goods_desc = UEditorField(verbose_name='内容', imagePath='goods/images/', width=1000, height=300, filePath='goods/files/', default='')
    ship_free = models.BooleanField(default=True, verbose_name='是否承担运费')
    goods_front_image = models.ImageField(upload_to='', null=True, blank=True, verbose_name='封面图')
    is_new = models.BooleanField(default=False, verbose_name='是否新品')
    is_hot = models.BooleanField(default=False, verbose_name='是否热销')
    
    add_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name
        
        
class GoodsImage(models.Model):
    """
    商品轮播图:
    """
    goods = models.ForeignKey(Goods, verbose_name='商品', related_name="images")
    image = models.ImageField(upload_to='', verbose_name='图片', null=True, blank=True)
    image_url = models.CharField(max_length=300, null=True, blank=True, verbose_name='图片地址')
    
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    
    def __str__(self):
        return self.goods.name
    
    class Meta:
        verbose_name = '商品轮播图'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    """
    轮播的商品
    """
    goods = models.ForeignKey(Goods, verbose_name='商品')
    image = models.ImageField(upload_to='banner', verbose_name='轮播图')
    index = models.IntegerField(default=0, verbose_name='轮播顺序')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.goods.name

    class Meta:
        verbose_name = '轮播商品'
        verbose_name_plural = verbose_name

```

