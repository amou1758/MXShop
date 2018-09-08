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
