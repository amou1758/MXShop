
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
        






"""
项目原始资料
import sys
import os


pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MxShop.settings")

import django
django.setup()

from goods.models import Goods, GoodsCategory, GoodsImage

from db_tools.data.product_data import row_data

for goods_detail in row_data:
    goods = Goods()
    goods.name = goods_detail["name"]
    goods.market_price = float(int(goods_detail["market_price"].replace("￥", "").replace("元", "")))
    goods.shop_price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", "")))
    goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] is not None else ""
    goods.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
    goods.goods_front_image = goods_detail["images"][0] if goods_detail["images"] else ""

    category_name = goods_detail["categorys"][-1]
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    goods.save()

    for goods_image in goods_detail["images"]:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.goods = goods
        goods_image_instance.save()

"""