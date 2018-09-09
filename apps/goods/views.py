from rest_framework import generics, mixins
from rest_framework.pagination import PageNumberPagination
# 重构我们的 分页功能
from rest_framework import viewsets
from rest_framework import filters
# 使用 DRF 的 filters
from goods.models import Goods
from .serializers import GoodsSerializer
# 导入过滤器模块
from django_filters.rest_framework import DjangoFilterBackend
from .filter import GoodsFilter

class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin,  viewsets.GenericViewSet):
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
    ordering_fields = ('sold_num', 'add_time')
    # 指定排序的字段