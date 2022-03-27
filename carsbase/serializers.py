from rest_framework import serializers
from .models import *
# from datetime import date


class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = '__all__'


class BrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = '__all__'


class ModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Models
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
#         # fields = ('color', 'model', 'count', 'order_date')


# class OrdersSerializerList(serializers.Serializer):
#     order_date = serializers.DateField(default=date.today)
#     color = serializers.CharField(max_length=100)
#     brand = serializers.CharField(max_length=100)
#     model = serializers.CharField(max_length=100)
#     count = serializers.IntegerField()