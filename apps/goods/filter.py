import django_filters

from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    # 对商品进行最大值和最小值的行为
    price_min = django_filters.NumberFilter(name='shop_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(name='shop_price', lookup_expr='lte')
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')
    # 关于字符串的模糊查询, name='name' 指定字段 lookup_expr='icontains',
    # contaions: 区分大小写
    # icontains: 不区分大小写

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'name']