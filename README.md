#Django-REST-Framework 的应用

### 1. 项目初始化

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



### 2. user model 设计:

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



### 3. goods models 设计:

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
    category_category = models.ForeignKey("self", null=True, blank=True,  max_length=20, verbose_name='父类级别', related_name='sub_cat')
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
    image = models.ImageField(max_length=200, upload_to='brand/images/', verbose_name='上传图片')
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



### 4. Trade Models 设计:

```python
from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
# 获取 UserApp中的Model, 推荐使用这种软编码形式
from goods.models import Goods
User = get_user_model()


class ShoppingCart(models.Model):
    """
    购物车:
    """
    user = models.ForeignKey(User, verbose_name='用户', help_text='用户')
    goods = models.ForeignKey(Goods, verbose_name='商品', help_text='商品')
    goods_num = models.IntegerField(default=0, verbose_name='商品数量', help_text='商品数量')
    
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    
    def __str__(self):
        return self.goods.name
    
    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
    
    
class OrderInfo(models.Model):
    """
    订单
    """
    ORDER_STATUS = (
        ('success', "成功"),
        ('cancel', "取消"),
        ('cancel', "待支付")
    )
    user = models.ForeignKey(User, verbose_name='用户', help_text='用户')
    order_sn = models.CharField(max_length=30, verbose_name='订单编号')
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='支付宝订单号')
    # 第三方支付: 支付宝支付的订单号与我们的商品的订单号做一个关联
    pay_status = models.CharField(max_length=20, choices=ORDER_STATUS, verbose_name='支付状态')
    post_script = models.CharField(max_length=200, verbose_name='订单留言')
    order_mount = models.FloatField(verbose_name='订单金额')
    pay_time = models.DateTimeField(null=True, blank=True, default=datetime.now, verbose_name='支付时间')
    
    # 用户中心
    address = models.CharField(max_length=200, verbose_name='签收地址')
    signer_name = models.CharField(max_length=20, verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11, verbose_name='签收电话')
    
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    
    def __str__(self):
        return str(self.order_sn)
    # 返回商品的订单编号
    
    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name
    
    
class OrderGoods(models.Model):
    """
    订单的商品详情
    """
    order = models.ForeignKey(OrderInfo, verbose_name='订单信息')
    goods = models.ForeignKey(Goods, verbose_name='商品')
    goods_num = models.IntegerField(default=0, verbose_name='商品数量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    
    def __str__(self):
        return str(self.order.order_sn)
        # 返回订单编号
    
    class Meta:
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

```



#### 5. get_user_model() 获取用户模型

**下面为 get_user_model() 函数的源码, 当然–> 如果想用该函数获取项目中的用户模型  需要在 settings 中配置用户模型的路径, 以便我们 django  能够找到**

```python
# get_user_model() 函数的源码:
def get_user_model():
    """
    Returns the User model that is active in this project.
    """
    
    try:
        return django_apps.get_model(settings.AUTH_USER_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("AUTH_USER_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL refers to model '%s' that has not been installed" % settings.AUTH_USER_MODEL
        )
```

#### 在 settings.py 配置文件中 配置我们的用户模型

```python
# 需要我们在 settings 中配置 UserProfile
# 下面就是在settings中的配置
# 将User表中的字段替换掉系统中的用户
AUTH_USER_MODEL = 'user.UserProfile'
```

### User_Operation_App(用户操作) Models 

```python
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

from goods.models import Goods

User = get_user_model()


class UserFav(models.Model):
    """
    用户收藏:
    """
    user = models.ForeignKey(User, verbose_name='用户')
    goods = models.ForeignKey(Goods, verbose_name='商品')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    
    def __str__(self):
        return self.user.name
    # 返回用户收藏的商品编号
    
    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserLeavingMessage(models.Model):
    """
    用户留言:
    """
    MESSAGE_CHOICES = (
        (1, '留言'),
        (2, '投诉'),
        (3, '询问'),
        (4, '售后'),
        (5, '求购'),
    )
    user = models.ForeignKey(User, verbose_name='用户')
    msg_type = models.IntegerField(default=1, choices=MESSAGE_CHOICES, verbose_name='留言类型', help_text="留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)")
    subject = models.CharField(max_length=100, default='', verbose_name='主题')
    message = models.TextField(default='', verbose_name='留言内容', help_text='留言内容')
    file = models.FileField(upload_to='', verbose_name='上传的文件', help_text='上传的文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    
    def __str__(self):
        return self.subject
    
    class Meta:
        verbose_name = '用户留言'
        verbose_name_plural = verbose_name
        
        
class UserAddress(models.Model):
    """
    用户收获地址:
    """
    user = models.ForeignKey(User, verbose_name='用户')
    district = models.CharField(max_length=100, default='', verbose_name='区域') 
    address = models.CharField(max_length=100, default='', verbose_name='详细地址')
    signer_name = models.CharField(max_length=10, default='', verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11, default='', verbose_name='签收电话')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = '收获地址'
        verbose_name_plural = verbose_name
```



### 6. migrations 原理及表的生成:

**[传送门](https://www.bilibili.com/video/av30195311/?p=13)**



### 7. Xadmin 后台管理的配置.

官方的 xadmin 对于 python36 会有bug

用项目的 xadmin 代替官方的

#### 1. github 搜索xadmin 查看官方的依赖包

- 依赖包在 requirements.txt 内记录.

![1536315472210](C:\Users\Administrator\AppData\Local\Temp\1536315472210.png)

**requiretments.txt 文件记录如下:**

```python
django>=1.9.0
django-crispy-forms>=1.6.0
django-import-export>=0.5.1
django-reversion>=2.0.0
django-formtools==1.0
future==0.15.2
httplib2==0.9.2
six==1.10.0
```

除了django, 其他依赖包都要安装, 依赖包直接用最新版本的就可以

**安装好之后  依赖包信息如下:**

```python
Successfully installed 
diff-match-patch-20121119 
django-crispy-forms-1.7.2 
django-formtools-2.1 
django-import-export-1.0.1 
django-reversion-3.0.0 
et-xmlfile-1.0.1
future-0.16.0 httpl
ib2-0.11.3 
jdcal-1.4 
odfpy-1.3.6 
openpyxl-2.5.6 
pyyaml-3.13 
six-1.11.0 
tablib-0.12.1
unicodecsv-0.14.1 
xlrd-1.1.0 
xlwt-1.3.0

```

#### 还要安装 xls, xlsx 导出文件依赖包

![1536316011774](C:\Users\Administrator\AppData\Local\Temp\1536316011774.png)这两个依赖包是用于导出 excel 文件的



#### 在后台修改 App 的现实名称:

```PYTHON
from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'apps.user'
    verbose_name = '用户管理'
# 在 App 的 apps.py 的文件中添加 verbose_name 的字段即可
```

