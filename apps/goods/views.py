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
    
