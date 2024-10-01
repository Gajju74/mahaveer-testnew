# serializer.py 

from rest_framework import serializers
from .models import Category, StockItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class StockItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = StockItem
        fields = [
            'id', 'code', 'kundan', 'moti', 'po', 'nw', 'gw', 'pcs', 
            'k_amt', 'm_amt', 'p_amt', 'supplier',
            'category', 'category_name', 'image'
        ]

    def create(self, validated_data):
        category_name = validated_data.pop('category_name', None)
        if category_name:
            category = Category.objects.get(name=category_name)
            validated_data['category'] = category

        return StockItem.objects.create(**validated_data)

