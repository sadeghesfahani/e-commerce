from attr.filters import exclude
from rest_framework import serializers

from store.models import Product, Category, TemporaryBasket, Coupon, Address, Order, ProductOrder, Slider


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


class TemporaryBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryBasket
        exclude = ('user',)


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('user',)


class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        exclude = ('user',)


class OrderSerializer(serializers.ModelSerializer):
    products = ProductOrderSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    @staticmethod
    def get_total(obj):
        return obj.total



class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'