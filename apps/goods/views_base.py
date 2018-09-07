# Django 中的 ListView
from django.views.generic.base import View
from django.views.generic import ListView

from goods.models import Goods


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
