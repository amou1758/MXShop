from rest_framework import serializers
from goods.models import Goods, GoodsCategory



class CategorySerializer3(serializers.ModelSerializer):
    """目的:  取出该分类的子类"""
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)
    """目的:  取出该分类的子类"""
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)
    # many=True 表示可能会有多个字段
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    # 对GoodsCategorySerializer 进行实例化, 也就是说将我们的外键表, 进行序列化之后, 引入进来进行实例化之后, 就可以当作我们的外键使用了
    
    class Meta:
        model = Goods
        fields = '__all__'
