#Django-REST-Framework 的应用

## DRF

#### DRF: 一个强大的web API

- **Django REST FrameWork中文文档目录：**

  [Django REST FrameWork 中文教程1:序列化](http://www.chenxm.cc/post/289.html)

  [Django REST FrameWork 中文教程2:请求和响应](http://www.chenxm.cc/post/290.html)

  [Django REST FrameWork 中文教程3:基于类的视图](http://www.chenxm.cc/post/291.html)

  [Django REST FrameWork 中文教程4：验证和权限](http://www.chenxm.cc/post/292.html)

  [Django REST FrameWork 中文教程5：关系和超链接API](http://www.chenxm.cc/post/293.html)

  [Django REST FrameWork 中文教程6: ViewSets＆Routers](http://www.chenxm.cc/post/294.html)

  [Django REST FrameWork 中文教程7：模式和客户端库](http://www.chenxm.cc/post/295.html)

DRF: 支持的版本:

REST framework requires the following:

- Python (2.7, 3.2, 3.3, 3.4, 3.5, 3.6)
- Django (1.10, 1.11, 2.0)

The following packages are optional:

- [coreapi](https://pypi.org/project/coreapi/) (1.32.0+) - Schema generation support.
- [Markdown](https://pypi.org/project/Markdown/) (2.1.0+) - Markdown support for the browsable API.
- [django-filter](https://pypi.org/project/django-filter/) (1.0.1+) - Filtering support.
- [django-crispy-forms](https://github.com/maraujop/django-crispy-forms) - Improved HTML display for filtering.
- [django-guardian](https://github.com/django-guardian/django-guardian) (1.1.1+) - Object level permissions support.



## 第一章: 项目初始化配置

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



### 8. 利用 Django models 将数据导入:

- 先获取当前脚本的路径

- 在获取项目的目录

- 导入 项目settings.py (导入项目的配置文件)

- 初始化 Django

- 导入 models 中的模型类

- 进行插入数据

- ```python
  
  # 独立使用 django-model
  import os
  import sys
  
  # 获取当前脚本的路径
  pwd = os.path.dirname(os.path.realpath(__file__))
  # 获取项目的根目录
  sys.path.append(pwd+"../")
  # 找到项目 setting 文件, 获取setting中的配置, 初始化Django
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MXShop.settings")
  
  import django
  django.setup()
  
  # 先初始化 Django  在导入项目的中的模型
  # 导入models模型
  from goods.models import GoodsCategory
  
  # 数据存储的位置
  from db_tools.data.category_data import row_data
  
  
  # 入库
  for lev1_cat in row_data:
      lev1_intance = GoodsCategory()
      lev1_intance.code = lev1_cat["code"]
      lev1_intance.name = lev1_cat["name"]
      lev1_intance.category_type = 1
      lev1_intance.save()
      
      for lev2_cat in lev1_cat['sub_categorys']:
          lev2_intance = GoodsCategory()
          lev2_intance.code = lev2_cat["code"]
          lev2_intance.name = lev2_cat["name"]
          lev2_intance.category_type = 2
          lev2_intance.parent_category = lev1_intance
          lev2_intance.save()
          
          for lev3_cat in lev2_cat['sub_categorys']:
              lev3_intance = GoodsCategory()
              lev3_intance.code = lev3_cat["code"]
              lev3_intance.name = lev3_cat["name"]
              lev3_intance.category_type = 3
              lev3_intance.parent_category = lev2_intance
              lev3_intance.save()
  ```



### 9. 导入商品和商品类别数据(Django-Admin)

#### 导入数据思路和操作 与 第8小章 相同

```python

# 独立使用 django-model
import os
import sys

# 获取当前脚本的路径
pwd = os.path.dirname(os.path.realpath(__file__))
# 获取项目的根目录
sys.path.append(pwd+"../")
# 找到项目 setting 文件, 获取setting中的配置, 初始化Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MXShop.settings")

import django
django.setup()

# 先初始化 Django  在导入项目的中的模型
# 导入models模型
from goods.models import Goods, GoodsCategory, GoodsImage
# 导入数据
from db_tools.data.product_data import row_data


for goods_detail in row_data:
    goods = Goods()
    goods.name = goods_detail['name']
    goods.market_price = float(int(goods_detail["market_price"].replace("￥", "").replace("元", "")))
    goods.shop_price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", "")))
    goods.goods_brief = goods_detail['desc'] if goods_detail['desc'] is not None else ""
    goods.goods_desc = goods_detail['goods_desc'] if goods_detail['goods_desc'] is not None else ""
    goods.goods_front_image = goods_detail['images'][0] if goods_detail['images'] is not None else ""
    category_name = goods_detail['categorys'][-1]
    
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
        
    goods.save()
    
    for goods_image in goods_detail['images']:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.goods = goods
        goods_image_instance.save()
        
```

#### 导入数据完毕后:

数据库内部存储的图片实际上是图片存储的路径, 我们的图片等静态资源存放在 media 文件夹内部, 

#### 配置 Media:

##### 配置 settings.py 文件

```python

# 如果不设置此项配置, Django无法找到我们存放的图片
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

```

##### 配置 urls.py 文件

也就是外部访问我们服务器内部的图片资源的 url 

```python
# 设计静态文件的访问url
from MXShop.settings import MEDIA_ROOT
from django.views.static import serve
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]
```

#### 跟 后台富文本编辑器的配置相似



## 第二章: RESTful 简单介绍:

### 1. restful 和 前端源码结构介绍 [传送门](https://www.bilibili.com/video/av30195311/?p=17)

#### 前后端分离优缺点:

##### 为什么要前后端分离:

1. **pc, app, pad 多端适应**
2. **SPA(单页面[后端提供数据, 前端显示]) 开发模式开发流行**
3. **前后端开发职责不清**
4. **开发效率问题, 前后端相互等待**
5. **前端一直配合后端, 能力受限**
6. **后台开发语言和模版高度耦合, 导致开发语言依赖严重**

##### 前后端分离缺点:

1. 前后端学习门槛增加
2. 数据依赖导致文档重要性增加
3. 前端工作量加大
4. SEO(搜索引擎的排名) 难度加大
5. 后端开发模式迁移增加成本

#### RESTFUL_API

- restful api 目前是前后端分离最佳实践(也就是前后端分离的一个标准)

  - 轻量, 直接通过 http, 不需要额外的协议, post/get/delete操作
  - 面向资源(利用url来进行资源的CRUD), 一目了然, 具有自解释性



### 阮一峰 RESTful 构架的理解

越来越多的人开始意识到，**网站即软件**，而且是一种新型的软件。

这种"互联网软件"采用客户端/服务器模式，建立在分布式体系上，通过互联网通信，具有高延时（high latency）、高并发等特点。

网站开发，完全可以采用软件开发的模式。但是传统上，软件和网络是两个不同的领域，很少有交集；软件开发主要针对单机环境，网络则主要研究系统之间的通信。互联网的兴起，使得这两个领域开始融合，**现在我们必须考虑，如何开发在互联网环境中使用的软件。**

![img](http://www.ruanyifeng.com/blogimg/asset/201109/bg2011091202.jpg)

RESTful架构，就是目前最流行的一种互联网软件架构。它结构清晰、符合标准、易于理解、扩展方便，所以正得到越来越多网站的采用。

但是，到底什么是RESTful架构，并不是一个容易说清楚的问题。下面，我就谈谈我理解的RESTful架构。

**一、起源**

REST这个词，是[Roy Thomas Fielding](http://en.wikipedia.org/wiki/Roy_Fielding)在他2000年的[博士论文](http://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)中提出的。

![img](http://www.ruanyifeng.com/blogimg/asset/201109/bg2011091201.jpg)

Fielding是一个非常重要的人，他是HTTP协议（1.0版和1.1版）的主要设计者、Apache服务器软件的作者之一、Apache基金会的第一任主席。所以，他的这篇论文一经发表，就引起了关注，并且立即对互联网开发产生了深远的影响。

他这样介绍论文的写作目的：

> "本文研究计算机科学两大前沿----软件和网络----的交叉点。长期以来，软件研究主要关注软件设计的分类、设计方法的演化，很少客观地评估不同的设计选择对系统行为的影响。而相反地，网络研究主要关注系统之间通信行为的细节、如何改进特定通信机制的表现，常常忽视了一个事实，那就是改变应用程序的互动风格比改变互动协议，对整体表现有更大的影响。**我这篇文章的写作目的，就是想在符合架构原理的前提下，理解和评估以网络为基础的应用软件的架构设计，得到一个功能强、性能好、适宜通信的架构。**"
>
> (This dissertation explores a junction on the frontiers of two research disciplines in computer science: software and networking. Software research has long been concerned with the categorization of software designs and the development of design methodologies, but has rarely been able to objectively evaluate the impact of various design choices on system behavior. Networking research, in contrast, is focused on the details of generic communication behavior between systems and improving the performance of particular communication techniques, often ignoring the fact that changing the interaction style of an application can have more impact on performance than the communication protocols used for that interaction. My work is motivated by the desire to understand and evaluate the architectural design of network-based application software through principled use of architectural constraints, thereby obtaining the functional, performance, and social properties desired of an architecture. )

#### **二、名称**

Fielding将他对互联网软件的架构原则，定名为REST，即Representational State Transfer的缩写。我对这个词组的翻译是"表现层状态转化"。

如果一个架构符合REST原则，就称它为RESTful架构。

**要理解RESTful架构，最好的方法就是去理解Representational State Transfer这个词组到底是什么意思，它的每一个词代表了什么涵义。**如果你把这个名称搞懂了，也就不难体会REST是一种什么样的设计。

#### **三、资源（Resources）**

REST的名称"表现层状态转化"中，省略了主语。"表现层"其实指的是"资源"（Resources）的"表现层"。

**所谓"资源"，就是网络上的一个实体，或者说是网络上的一个具体信息。**它可以是一段文本、一张图片、一首歌曲、一种服务，总之就是一个具体的实在。你可以用一个URI（统一资源定位符）指向它，每种资源对应一个特定的URI。要获取这个资源，访问它的URI就可以，因此URI就成了每一个资源的地址或独一无二的识别符。

所谓"上网"，就是与互联网上一系列的"资源"互动，调用它的URI。

#### **四、表现层（Representation）**

"资源"是一种信息实体，它可以有多种外在表现形式。**我们把"资源"具体呈现出来的形式，叫做它的"表现层"（Representation）。**

比如，文本可以用txt格式表现，也可以用HTML格式、XML格式、JSON格式表现，甚至可以采用二进制格式；图片可以用JPG格式表现，也可以用PNG格式表现。

URI只代表资源的实体，不代表它的形式。严格地说，有些网址最后的".html"后缀名是不必要的，因为这个后缀名表示格式，属于"表现层"范畴，而URI应该只代表"资源"的位置。它的具体表现形式，应该在HTTP请求的头信息中用Accept和Content-Type字段指定，这两个字段才是对"表现层"的描述。

#### **五、状态转化（State Transfer）**

访问一个网站，就代表了客户端和服务器的一个互动过程。在这个过程中，势必涉及到数据和状态的变化。

互联网通信协议HTTP协议，是一个无状态协议。这意味着，所有的状态都保存在服务器端。因此，**如果客户端想要操作服务器，必须通过某种手段，让服务器端发生"状态转化"（State Transfer）。而这种转化是建立在表现层之上的，所以就是"表现层状态转化"。**

客户端用到的手段，只能是HTTP协议。具体来说，就是HTTP协议里面，四个表示操作方式的动词：GET、POST、PUT、DELETE。它们分别对应四种基本操作：**GET用来获取资源，POST用来新建资源（也可以用于更新资源），PUT用来更新资源，DELETE用来删除资源。**

#### **六、综述**

综合上面的解释，我们总结一下什么是RESTful架构：

　　（1）每一个URI代表一种资源；

　　（2）客户端和服务器之间，传递这种资源的某种表现层；

　　（3）客户端通过四个HTTP动词，对服务器端资源进行操作，实现"表现层状态转化"。

#### **七、误区**

RESTful架构有一些典型的设计误区。

**最常见的一种设计错误，就是URI包含动词。**因为"资源"表示一种实体，所以应该是名词，URI不应该有动词，动词应该放在HTTP协议中。

举例来说，某个URI是/posts/show/1，其中show是动词，这个URI就设计错了，正确的写法应该是/posts/1，然后用GET方法表示show。

如果某些动作是HTTP动词表示不了的，你就应该把动作做成一种资源。比如网上汇款，从账户1向账户2汇款500元，错误的URI是：

> 　　POST /accounts/1/transfer/500/to/2

正确的写法是把动词transfer改成名词transaction，资源不能是动词，但是可以是一种服务：

> 　　POST /transaction HTTP/1.1
> 　　Host: 127.0.0.1
> 　　
> 　　from=1&to=2&amount=500.00

**另一个设计误区，就是在URI中加入版本号**：

> 　　http://www.example.com/app/1.0/foo
>
> 　　http://www.example.com/app/1.1/foo
>
> 　　http://www.example.com/app/2.0/foo

因为不同的版本，可以理解成同一种资源的不同表现形式，所以应该采用同一个URI。版本号可以在HTTP请求头信息的Accept字段中进行区分（参见[Versioning REST Services](http://www.informit.com/articles/article.aspx?p=1566460)）：

> 　　Accept: vnd.example-com.foo+json; version=1.0
>
> 　　Accept: vnd.example-com.foo+json; version=1.1
>
> 　　Accept: vnd.example-com.foo+json; version=2.0



### 阮一峰 RESTful API 设计指南





作者： [阮一峰](http://www.ruanyifeng.com)

日期： [2014年5月22日](http://www.ruanyifeng.com/blog/2014/05/)

  [   ![珠峰培训](http://www.ruanyifeng.com/blog/images/0asddeewr1.png) ](http://www.zhufengpeixun.cn/main/index.html?ref=ruanyifeng) 

网络应用程序，分为前端和后端两个部分。当前的发展趋势，就是前端设备层出不穷（手机、平板、桌面电脑、其他专用设备......）。

因此，必须有一种统一的机制，方便不同的前端设备与后端进行通信。这导致API构架的流行，甚至出现["API First"](http://www.google.com.hk/search?q=API+first)的设计思想。[RESTful API](http://en.wikipedia.org/wiki/Representational_state_transfer)是目前比较成熟的一套互联网应用程序的API设计理论。我以前写过一篇[《理解RESTful架构》](http://www.ruanyifeng.com/blog/2011/09/restful.html)，探讨如何理解这个概念。

今天，我将介绍RESTful API的设计细节，探讨如何设计一套合理、好用的API。我的主要参考了两篇文章（[1](http://codeplanet.io/principles-good-restful-api-design/)，[2](https://bourgeois.me/rest/)）。

![RESTful API](http://www.ruanyifeng.com/blogimg/asset/2014/bg2014052201.png)

#### 一、协议

API与用户的通信协议，总是使用[HTTPs协议](http://www.ruanyifeng.com/blog/2014/02/ssl_tls.html)。

#### 二、域名

应该尽量将API部署在专用域名之下。

> ```javascript
> https://api.example.com
> ```

如果确定API很简单，不会有进一步扩展，可以考虑放在主域名下。

> ```javascript
> https://example.org/api/
> ```

#### 三、版本（Versioning）

应该将API的版本号放入URL。

> ```javascript
> https://api.example.com/v1/
> ```

另一种做法是，将版本号放在HTTP头信息中，但不如放入URL方便和直观。[Github](https://developer.github.com/v3/media/#request-specific-version)采用这种做法。

#### 四、路径（Endpoint）

路径又称"终点"（endpoint），表示API的具体网址。

在RESTful架构中，每个网址代表一种资源（resource），所以网址中不能有动词，只能有名词，而且所用的名词往往与数据库的表格名对应。一般来说，数据库中的表都是同种记录的"集合"（collection），所以API中的名词也应该使用复数。

举例来说，有一个API提供动物园（zoo）的信息，还包括各种动物和雇员的信息，则它的路径应该设计成下面这样。

> - https://api.example.com/v1/zoos
> - https://api.example.com/v1/animals
> - https://api.example.com/v1/employees

#### 五、HTTP动词

对于资源的具体操作类型，由HTTP动词表示。

常用的HTTP动词有下面五个（括号里是对应的SQL命令）。

> - GET（SELECT）：从服务器取出资源（一项或多项）。
> - POST（CREATE）：在服务器新建一个资源。
> - PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
> - PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
> - DELETE（DELETE）：从服务器删除资源。

还有两个不常用的HTTP动词。

> - HEAD：获取资源的元数据。
> - OPTIONS：获取信息，关于资源的哪些属性是客户端可以改变的。

下面是一些例子。

> - GET /zoos：列出所有动物园
> - POST /zoos：新建一个动物园
> - GET /zoos/ID：获取某个指定动物园的信息
> - PUT /zoos/ID：更新某个指定动物园的信息（提供该动物园的全部信息）
> - PATCH /zoos/ID：更新某个指定动物园的信息（提供该动物园的部分信息）
> - DELETE /zoos/ID：删除某个动物园
> - GET /zoos/ID/animals：列出某个指定动物园的所有动物
> - DELETE /zoos/ID/animals/ID：删除某个指定动物园的指定动物

#### 六、过滤信息（Filtering）

如果记录数量很多，服务器不可能都将它们返回给用户。API应该提供参数，过滤返回结果。

下面是一些常见的参数。

> - ?limit=10：指定返回记录的数量
> - ?offset=10：指定返回记录的开始位置。
> - ?page=2&per_page=100：指定第几页，以及每页的记录数。
> - ?sortby=name&order=asc：指定返回结果按照哪个属性排序，以及排序顺序。
> - ?animal_type_id=1：指定筛选条件

参数的设计允许存在冗余，即允许API路径和URL参数偶尔有重复。比如，GET /zoo/ID/animals 与 GET /animals?zoo_id=ID 的含义是相同的。

#### 七、状态码（Status Codes）

服务器向用户返回的状态码和提示信息，常见的有以下一些（方括号中是该状态码对应的HTTP动词）。

> - 200 OK - [GET]：服务器成功返回用户请求的数据，该操作是幂等的（Idempotent）。
> - 201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。
> - 202 Accepted - [*]：表示一个请求已经进入后台排队（异步任务）
> - 204 NO CONTENT - [DELETE]：用户删除数据成功。
> - 400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
> - 401 Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）。
> - 403 Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的。
> - 404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
> - 406 Not Acceptable - [GET]：用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。
> - 410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的。
> - 422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误。
> - 500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功。

状态码的完全列表参见[这里](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)。

#### 八、错误处理（Error handling）

如果状态码是4xx，就应该向用户返回出错信息。一般来说，返回的信息中将error作为键名，出错信息作为键值即可。

> ```javascript
> {
>     error: "Invalid API key"
> }
> ```

#### 九、返回结果

针对不同操作，服务器向用户返回的结果应该符合以下规范。

> - GET /collection：返回资源对象的列表（数组）
> - GET /collection/resource：返回单个资源对象
> - POST /collection：返回新生成的资源对象
> - PUT /collection/resource：返回完整的资源对象
> - PATCH /collection/resource：返回完整的资源对象
> - DELETE /collection/resource：返回一个空文档

#### 十、Hypermedia API

RESTful API最好做到Hypermedia，即返回结果中提供链接，连向其他API方法，使得用户不查文档，也知道下一步应该做什么。

比如，当用户向api.example.com的根目录发出请求，会得到这样一个文档。

> ```javascript
> {"link": {
>   "rel":   "collection https://www.example.com/zoos",
>   "href":  "https://api.example.com/zoos",
>   "title": "List of zoos",
>   "type":  "application/vnd.yourformat+json"
> }}
> ```

上面代码表示，文档中有一个link属性，用户读取这个属性就知道下一步该调用什么API了。rel表示这个API与当前网址的关系（collection关系，并给出该collection的网址），href表示API的路径，title表示API的标题，type表示返回类型。

Hypermedia API的设计被称为[HATEOAS](http://en.wikipedia.org/wiki/HATEOAS)。Github的API就是这种设计，访问[api.github.com](https://api.github.com/)会得到一个所有可用API的网址列表。

> ```javascript
> {
>   "current_user_url": "https://api.github.com/user",
>   "authorizations_url": "https://api.github.com/authorizations",
>   // ...
> }
> ```

从上面可以看到，如果想获取当前用户的信息，应该去访问[api.github.com/user](https://api.github.com/user)，然后就得到了下面结果。

> ```javascript
> {
>   "message": "Requires authentication",
>   "documentation_url": "https://developer.github.com/v3"
> }
> ```

上面代码表示，服务器给出了提示信息，以及文档的网址。

#### 十一、其他

（1）API的身份认证应该使用[OAuth 2.0](http://www.ruanyifeng.com/blog/2014/05/oauth_2_0.html)框架。

（2）服务器返回的数据格式，应该尽量使用JSON，避免使用XML。

（完）





### 2. vue 的基本概念介绍 [传送门](https://www.bilibili.com/video/av30195311/?p=18)

1. 前端工程化
2. 数据双向绑定
3. 组件化开发

**vue 开发的几个概念:**

1. webpack, 将所有的东西变成 js 文件(web动态显示)
2. vue, vuex(组件间通信), vue-router(路径与组件进行关联), axios(在 vue中替代 ajax)
   1. mvvm: 不推荐 js 操作 DOM书,  axios代替 jquery 包 提高执行效率
3. ES6, babel
   1. babel:转化器, 将ES6语法转换成ES5语法



## 第三章: 商品列表页

### django 的 view 实现商品列表页:

```python
# cbv  --> class base view 面相对象的编程方式
```

**Django–ListView**

```
from django.views.generic.base import View
# 导入 django 中的 view
```

**自己编写 djangolistview 来返回商品列表页数据:**

```python
# Django 中的 ListView
from django.views.generic.base import View
# View, ListView 是 Django 为我们提供的 类视图函数, 相同的类视图函数还有很多
from django.views.generic import ListView

from goods.models import Goods
# 导入我们的视图

class GoodsListView(View):
    def get(self, request):
        """
        通过 django 的 view 实现商品列表页
        :param request:
        :return:json.dumps(xxx)
        """
        json_list = []
        goods = Goods.objects.all()[:10]
        for good in goods:
            json_dict = {}
            json_dict['name'] = good.name
            json_dict['category'] = good.category.name
            json_dict['market_price'] = good.market_price
            json_list.append(json_dict)
        print(json_list)
        from django.http import HttpResponse
        import json
        return HttpResponse(json.dumps(json_list), content_type='application/json')
    # 需要指定返回数据的格式: content_type='application/json'
    # json.dumps() 将数据 json 序列化

```

**json 不能对 datetime 数据进行序列化**

#### **model_to_dict() 对象转字典函数:**

```python
        json_list = []
        goods = Goods.objects.all()[:10]
        # 只取结果集中的前十条数据
        for good in goods:
            json_dict = {}
            json_dict['name'] = good.name
            json_dict['category'] = good.category.name
            json_dict['market_price'] = good.market_price
            json_dict['add_time'] = good.add_time
            json_list.append(json_dict)
        ## 上下两者等效  
        from django.forms.models import model_to_dict
        for good in goods:
            json_dict = model_to_dict(good)
            json_list.append(json_dict)
```



### 2. Django 的 serializer 序列化 model [传送门](https://www.bilibili.com/video/av30195311/?p=21)

使用 Django 的 serializer 

```python
from django.views.generic.base import View

from goods.models import Goods


class GoodsListView(View):
    def get(self, request):
        """
        通过 django 的 view 实现商品列表页
        """
        goods = Goods.objects.all()[:10]
        import json
        from django.core import serializers
        # django 为我们提供的 serializers方法, 专门做序列化的
        json_data = serializers.serialize('json', goods)
        # 将 goods 对象 按照 json 格式进行序列化
        json_data = json.loads(json_data)
        # 将数据进行解码, 将 json 数据变成 py 的 dict 对象
        from django.http import JsonResponse
        # JsonResponse 以 json 形式返回, safe=False 告诉django不要转义
        return JsonResponse(json_data, safe=False)
```

#### serializers将我们的数据进行序列化 

`serializers.py`

```python
from rest_framework import serializers
from rest_framework.response import Response
# Response 是 DRF 为我们封装的相应函数(在DJango的Response的基础上做了封装)
from rest_framework import status

from goods.models import Goods, GoodsCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    """
    ModelSerializer: 会根据我们的模型类, 分析其类型, 然后做映射
    """
    category = CategorySerializer()
    # 实例化 GoodsCategory 序列化之后的结果
    class Meta:
        model = Goods
        # fields = ('name', 'click_num', 'market_price', 'add_time')
        # fields 指定要序列换的字段, fields 中有个 '__all__' 属性, 表示所有字段全部序列化(变成字符串)
        fields = '__all__'    
```

#### 取出序列化的数据进行响应

`views.py`

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import GoodsSerializer

from .models import Goods


class GoodsListView(APIView):
    """
    List all goods
    """

    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data)
```



### 3. ApiView 方式实现商品列表页: [传送门](https://www.bilibili.com/video/av30195311/?p=22)



#### 在项目的 urls.py 中配置 DRF 的登陆 url

```python
 url(r'^api-auth/', include('rest_framework.urls')),
```



![1536354074457](C:\Users\Administrator\AppData\Local\Temp\1536354074457.png)![1536354098990](C:\Users\Administrator\AppData\Local\Temp\1536354098990.png)

##### 主要的错误原因是: DRF 中可以登陆, 然而返回的是一个空的用户名  所以…

在 models 中定义的 user 表 中返回的 name 字段可以为空

```python

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
    
    def __str__(self):
        return self.username
    # 将 self.name 字段 改为 username
    
```



### 4. DRF 的 modelsserializer 实现商品列表页功能

####  取出 前端传递过来的 post 的数据, 进行操作:

`serializers.py`

```python
from rest_framework import serializers
from goods.models import Goods


class GoodsSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=100)
    click_num = serializers.IntegerField(default=0)
    goods_front_image = serializers.ImageField()

    def create(self, validated_date):
        """
        重载 create 函数

        """
        # validated_date 会将 GoodsSerializer 的字段全部放到 dict 内
        return Goods.objects.create(**validated_date)

```

`views.py`

```python
    def post(self, request):
        """
        request: DRF 为我们封装的
        :param request:
        """
        serializer = GoodsSerializer(data=request.data)
        # request.data: DRF 将 post 的数据取出来
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.errors, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # status: Django 为我们提供的 HTTP 常用状态码
```

#### ModelSerializer 模型序列化

`serializers.py`

```python
from rest_framework import serializers
from goods.models import Goods


class GoodsSerializer(serializers.ModelSerializer):
    # ModelSerializer 将我们的模型(model)数据进行序列化
    class Meta:
        model = Goods
        # 指定我们的模型
        fields = ('name', 'click_num', 'market_price', 'add_time')
        # 指定我们的字段
        # fields 有一个 __all__ 属性表明: 模型中的所有字段全部序列化
        # fields = '__all__'
        
```

`views.py`

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import GoodsSerializer

from .models import Goods


class GoodsListView(APIView):
    """
    List all goods
    """

    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data)
```

ModelSerializer 模型序列化 使用外键

`serializers.py`

```python
from rest_framework import serializers
from goods.models import Goods, GoodsCategory


class GoodsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    category = GoodsCategorySerializer()
    # 对GoodsCategorySerializer 进行实例化, 也就是说将我们的外键表, 进行序列化之后, 引入进来进行实例化之后, 就可以当作我们的外键使用了
    
    class Meta:
        model = Goods
        fields = '__all__'
```

`views.py`

```python
from rest_framework.views import APIView
from rest_framework.response import Response

from goods.models import Goods
from .serializers import GoodsSerializer


class GoodsListView(APIView):
    """
    List all goods
    """

    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data)
```

**实现效果展示:**

![1536446168475](C:\Users\Administrator\AppData\Local\Temp\1536446168475.png)

### 5. GenericView 方式实现商品列表页和分页功能详解:

#### 使用 mixins.ListModelMixin generics.GenericAPIView

`serializers.py` 同上

`views.py`

```python
from rest_framework import mixins
from rest_framework import generics

from goods.models import Goods
from .serializers import GoodsSerializer


class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):
    """
    商品列表页
    mixins.ListModelMixin
    generics.GenericAPIView:

    """
    queryset = Goods.objects.all()[:10]
    #　得到我们的模型
    serializer_class = GoodsSerializer
    # 得到 我们的 模型的 Serializer
    
    def get(self, request, *args, **kwargs):
        # 如果我们不重载get 或者 post 的话, 他就会默认我们不接受 get 或者 post 的请求 ---> 可以使用ListView() 方法来解决这种问题
        # 重载 get 函数
        # get 函数 可以实现分页, 和 数据序列化
        return self.list(request, *args, **kwargs)
```

**如果我们不重载get 或者 post 的话, 他就会默认我们不接受 get 或者 post 的请求 ---> 可以使用ListView() 方法来解决这种问题**

#### **使用 ListView:**

```python
from rest_framework import generics

from goods.models import Goods
from .serializers import GoodsSerializer


class GoodsListView(generics.ListAPIView):
    """
    商品列表页
    """
    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializer
```

#### 使用分页:

**追加到项目的 settings.py 中即可**

```python
# 所有关于 rest_framework 的配置都有设定在这里
REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
}
```

**实现效果:**

![1536448406553](C:\Users\Administrator\AppData\Local\Temp\1536448406553.png)

#### 定制 Pagination 分页功能

**views.py**

```python
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
# 重构我们的 分页功能

from goods.models import Goods
from .serializers import GoodsSerializer


class GoodsPagination(PageNumberPagination):
    page_size = 40
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100

class GoodsListView(generics.ListAPIView):
    """
    商品列表页
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
```



### 6. viewsets 和 router 完成商品列表页: [传送门](https://www.bilibili.com/video/av30195311/?p=26)

viewset 提供的方法:

![1536456583014](C:\Users\Administrator\AppData\Local\Temp\1536456583014.png)

```python
"""
ViewSets are essentially just a type of class based view, that doesn't provide
any method handlers, such as `get()`, `post()`, etc... but instead has actions,
such as `list()`, `retrieve()`, `create()`, etc...

Actions are only bound to methods at the point of instantiating the views.

    user_list = UserViewSet.as_view({'get': 'list'})
    user_detail = UserViewSet.as_view({'get': 'retrieve'})

Typically, rather than instantiate views from viewsets directly, you'll
register the viewset with a router and let the URL conf be determined
automatically.

    router = DefaultRouter()
    router.register(r'users', UserViewSet, 'user')
    urlpatterns = router.urls
"""
from __future__ import unicode_literals

from functools import update_wrapper

from django.utils.decorators import classonlymethod
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, mixins, views


class ViewSetMixin(object):
    """
    This is the magic.

    Overrides `.as_view()` so that it takes an `actions` keyword that performs
    the binding of HTTP methods to actions on the Resource.

    For example, to create a concrete view binding the 'GET' and 'POST' methods
    to the 'list' and 'create' actions...

    view = MyViewSet.as_view({'get': 'list', 'post': 'create'})
    """

    @classonlymethod
    def as_view(cls, actions=None, **initkwargs):
        """
        Because of the way class based views create a closure around the
        instantiated view, we need to totally reimplement `.as_view`,
        and slightly modify the view function that is created and returned.
        """
        # The suffix initkwarg is reserved for identifying the viewset type
        # eg. 'List' or 'Instance'.
        cls.suffix = None

        # actions must not be empty
        if not actions:
            raise TypeError("The `actions` argument must be provided when "
                            "calling `.as_view()` on a ViewSet. For example "
                            "`.as_view({'get': 'list'})`")

        # sanitize keyword arguments
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r" % (
                    cls.__name__, key))

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            # We also store the mapping of request methods to actions,
            # so that we can later set the action attribute.
            # eg. `self.action = 'list'` on an incoming GET request.
            self.action_map = actions

            # Bind methods to actions
            # This is the bit that's different to a standard view
            for method, action in actions.items():
                handler = getattr(self, action)
                setattr(self, method, handler)

            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get

            # And continue as usual
            return self.dispatch(request, *args, **kwargs)

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())

        # We need to set these on the view function, so that breadcrumb
        # generation can pick out these bits of information from a
        # resolved URL.
        view.cls = cls
        view.initkwargs = initkwargs
        view.suffix = initkwargs.get('suffix', None)
        view.actions = actions
        return csrf_exempt(view)

    def initialize_request(self, request, *args, **kwargs):
        """
        Set the `.action` attribute on the view,
        depending on the request method.
        """
        request = super(ViewSetMixin, self).initialize_request(request, *args, **kwargs)
        method = request.method.lower()
        if method == 'options':
            # This is a special case as we always provide handling for the
            # options method in the base `View` class.
            # Unlike the other explicitly defined actions, 'metadata' is implicit.
            self.action = 'metadata'
        else:
            self.action = self.action_map.get(method)
        return request


class ViewSet(ViewSetMixin, views.APIView):
    """
    The base ViewSet class does not provide any actions by default.
    """
    pass


class GenericViewSet(ViewSetMixin, generics.GenericAPIView):
    """
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """
    pass


class ReadOnlyModelViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """
    pass


class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass

```



####  项目的 urls.py:

```python
from django.conf.urls import url, include
import xadmin

# 设计静态文件的访问url
from MXShop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

# 导入视图类
from goods.views import GoodsListViewSet


# 配置 goods 的 url
router = DefaultRouter()
router.register(r'goods', GoodsListViewSet)


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # 商品列表页 接口
    url(r'^', include(router.urls)),
    # 生成 DRF 自动文档的配置
    url(r'^docs/', include_docs_urls(title='慕学生鲜')),
    # 登陆 DRF 的 URL
    url(r'^api-auth/', include('rest_framework.urls')),
]

```

#### goods_app  的 views.py:

```python
from rest_framework import generics, mixins
from rest_framework.pagination import PageNumberPagination
# 重构我们的 分页功能
from rest_framework import viewsets

from goods.models import Goods
from .serializers import GoodsSerializer


class GoodsPagination(PageNumberPagination):
    page_size = 40
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100

class GoodsListViewSet(mixins.ListModelMixin,  viewsets.GenericViewSet):
    """
    商品列表页
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

```



### 7. DRF 的 APIView, GenericView, ViewSet 和 router 的原理分析: [传送门](https://www.bilibili.com/video/av30195311/?p=27)

理清思路: 继承关系

- GenericViewSet(viewset)  - DRF
  - GenericAPIView                   - DRF
    - APIView                                  - DRF
      - View                                          - Django

- mixin
  - CreateModelMixin
  - ListModelMixin
    - 将 get 和 list 链接起来 
  - UpdateModelMixin
    - 部分更新还是全部更新?
  - DestoryModelMixin
    - delete 方法
  - RetrieveModelMixin





