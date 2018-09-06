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
    pay_status = models.CharField(choices=ORDER_STATUS, verbose_name='支付状态')
    post_script = models.CharField(max_length=200, verbose_name='订单留言')
    order_mount = models.FloatField(verbose_name='订单金额')
    pay_time = models.DateTimeField(null=True, blank=True, default=datetime.now, verbose_name='支付时间')
    
    # 用户中心
    address = models.CharField(max_length=200, verbose_name='签收地址')
    signer_name = models.CharField(max_length=20, verbose_name='签收人')
    signer_mobile = models.CharField(verbose_name='签收电话')
    
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
    
    
    
    
    
"""
# get_user_model() 函数的源码:
def get_user_model():
    
    # Returns the User model that is active in this project.
    
    try:
        return django_apps.get_model(settings.AUTH_USER_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("AUTH_USER_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL refers to model '%s' that has not been installed" % settings.AUTH_USER_MODEL
        )

# 需要我们在 settings 中配置 UserProfile
# 下面就是在settings中的配置
# 将User表中的字段替换掉系统中的用户
AUTH_USER_MODEL = 'user.UserProfile'
"""