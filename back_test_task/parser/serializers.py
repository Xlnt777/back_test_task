from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id','name','shard','query','url', 'children']

    def get_children(self, obj):
        children = obj.children.all()
        if children:
            return CategorySerializer(children, many=True, context=self.context).data
        return []
    

class ProductSerializer(serializers.ModelSerializer):

    category = serializers.CharField(source='category.name')

    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'sale_price', 'rating', 'feedbacks', 'url']

    