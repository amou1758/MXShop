from rest_framework import generics, mixins
from rest_framework.pagination import PageNumberPagination
# 重构我们的 分页功能
from rest_framework import viewsets
from rest_framework import filters
# 使用 DRF 的 filters
from goods.models import Goods, GoodsCategory
from django_filters.rest_framework import DjangoFilterBackend
from .filter import GoodsFilter

from .serializers import GoodsSerializer, CategorySerializer
# 导入过滤器模块

class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表页, 分页, 搜索, 过滤, 排序
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # 指定过滤函数
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 指定 DRF 中的 SearchFilter, 进行字段的搜索
    # 指定 DRF 中的 OrderingFilter 进行字段的排序
    filter_class = GoodsFilter
    search_fields = ('^name', 'goods_brief', 'goods_desc')
    # 进行了三个字段的配置, 但是 ^ 表示, 必须存在 name 字段以你搜索的内容开头的
    # = 表示精确搜索, 使用方法同上
    ordering_fields = ('sold_num', 'shop_price')
    # 指定排序的字段
    
    
class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    """
    # 只需要在类视图中继承 mixins.RetrieveModelMixin  就可以在url中根据pk 取出具体某个数据
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer