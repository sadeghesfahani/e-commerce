from attr.filters import exclude
from django.db.models import Sum, Avg
from rest_framework import serializers

from store.models import Product, Category, TemporaryBasket, Coupon, Address, Order, ProductOrder, Slider, Comment, Favorit, Brand
from user.serializers import UserSerializer


class RelatedProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'main_image', 'final_price', 'featured', 'slug', 'remaining')


class ProductSerializer(serializers.ModelSerializer):
    sell = serializers.SerializerMethodField()
    related_products = RelatedProductsSerializer(many=True)
    rate = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    @staticmethod
    def get_sell(obj):
        quantity = ProductOrder.objects.filter(product=obj).annotate(Sum("quantity"))
        if len(quantity) > 0:
            return quantity[0].quantity__sum
        return 0

    @staticmethod
    def get_rate(obj):
        comments = Comment.objects.filter(rate__isnull=False, product=obj).aggregate(rate=Avg('rate'))
        return comments['rate'] / Comment.objects.filter(product=obj, rate__isnull=False).count() if comments['rate'] else 0

    @staticmethod
    def get_comments(obj):
        return CommentSerializer(Comment.objects.filter(product=obj), many=True, read_only=True).data


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


class CategoryWithBrandSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    brands = serializers.SerializerMethodField()

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

    @staticmethod
    def get_brands(obj):
        products_with_this_category = Product.objects.filter(category=obj)
        brands = Brand.objects.filter(product__in=products_with_this_category).distinct()
        return BrandSerializer(brands, many=True).data


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


class SimpleCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    to = SimpleCommentSerializer()
    like_number = serializers.SerializerMethodField()
    dislike_number = serializers.SerializerMethodField()
    user = UserSerializer(many=False)

    class Meta:
        model = Comment
        exclude = ['like', 'dislike']

    @staticmethod
    def get_like_number(obj):
        return obj.like.count()

    @staticmethod
    def get_dislike_number(obj):
        return obj.dislike.count()


class FavoritSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorit
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

    # def create(self, validated_data):
    #     print(validated_data)
    #     return Brand.objects.create(**validated_data)
