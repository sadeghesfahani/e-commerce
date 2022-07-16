from rest_framework import serializers

from store.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    @staticmethod
    def get_parent(obj):
        if obj.parent:
            return CategorySerializer(obj.parent).data
        else:
            return None

    @staticmethod
    def get_children(obj):
        if Category.objects.filter(parent=obj).exists():
            return SimpleCategorySerializer(Category.objects.filter(parent=obj), many=True).data
        else:
            return None
