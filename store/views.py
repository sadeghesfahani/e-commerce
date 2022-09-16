from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from store.category_manager import CategoryManager
from store.data_structures import ProductDataStructure, CategoryDataStructure, AddressDataStructure, CouponDataStructure
from store.models import Product, Category, TemporaryBasket, Coupon, Address, ProductOrder, Order, Slider, Comment, Favorit, Brand
from store.product_manager import ProductManager
from store.serializers import ProductSerializer, CategorySerializer, TemporaryBasketSerializer, CouponSerializer, AddressSerializer, OrderSerializer, \
    SliderSerializer, CommentSerializer, FavoritSerializer, BrandSerializer, CategoryWithBrandSerializer
from store.viewset_base import ViewSetBase


class SliderAPI(ViewSetBase):

    @staticmethod
    def create_slider(request):
        serializer = SliderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_sliders(request):
        sliders = SliderSerializer(Slider.objects.all(), many=True).data
        return Response(sliders)

    @staticmethod
    def edit_slider(request, slider_id):
        slider = get_object_or_404(Slider, pk=slider_id)
        serializer = SliderSerializer(slider, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete_slider(request, slider_id):
        slider = get_object_or_404(Slider, pk=slider_id)
        slider.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductAPI(ViewSetBase):

    def create_product(self, request):
        parameters = self.generate_parameters(request)
        structured_product = ProductDataStructure(**parameters)
        try:
            new_product = Product.objects.create(**structured_product.__dict__)
            new_product.save()
            return Response(ProductSerializer(new_product, many=False, read_only=True).data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex), "parameters": self.generate_parameters(request)},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def delete_product_id(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return ProductManager(product).delete()

    @staticmethod
    def delete_product_slug(request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        return ProductManager(product).delete()

    @staticmethod
    def get_all_products(request):
        products = Product.objects.all()
        return Response(ProductSerializer(products, many=True, read_only=True).data)

    @staticmethod
    def get_category_products_id(request, category_id):
        if Category.objects.filter(id=category_id).exists():
            products = Product.objects.filter(category_id=category_id)
            return Response(ProductSerializer(products, many=True, read_only=True).data)
        else:
            raise Http404

    @staticmethod
    def get_category_products_slug(request, category_slug):
        if Category.objects.filter(slug=category_slug).exists():
            products = Product.objects.filter(category__slug=category_slug)
            return Response(ProductSerializer(products, many=True, read_only=True).data)
        else:
            raise Http404

    @staticmethod
    def get_product_by_id(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return Response(ProductSerializer(product, many=False, read_only=True).data)

    @staticmethod
    def get_product_by_slug(request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        return Response(ProductSerializer(product, many=False, read_only=True).data)

    def edit_product_id(self, request, product_id):
        parameters = self.generate_parameters(request)
        product = get_object_or_404(Product, id=product_id)
        return ProductManager(product).edit(parameters)

    def edit_product_slug(self, request, product_slug):
        parameters = self.generate_parameters(request)
        product = get_object_or_404(Product, slug=product_slug)
        return ProductManager(product).edit(parameters)

    def get_permissions(self):
        if self.action == "create_product" or self.action == "edit_product_id" or self.action == "edit_product_slug" or self.action == "delete_product_id" or self.action == "delete_product_slug":
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super(ProductAPI, self).get_permissions()

    def search(self, request):
        parameters = self.generate_parameters(request)
        products_by_name = Product.objects.filter(name__icontains=parameters.get('search'))
        products_by_description = Product.objects.filter(description__icontains=parameters.get('search'))
        products = products_by_description | products_by_name
        return Response(ProductSerializer(products, many=True, read_only=True).data)

    @staticmethod
    def create_featured_product(request):
        return Response(ProductSerializer(Product.objects.filter(featured=True), many=True, read_only=True).data)

    @staticmethod
    def get_incredible_products(request):
        query_set = Product.objects.annotate(diff=F("price") - F("final_price"))
        new_query_set = query_set.filter(diff__gt=0)
        return Response(ProductSerializer(new_query_set, many=True, read_only=True).data)

    @staticmethod
    def get_products_of_a_brand(request, brand_id):
        return Response(ProductSerializer(Product.objects.filter(brand__id=brand_id), many=True, read_only=True).data)

class CategoryAPI(ViewSetBase):

    @staticmethod
    def get_category_id(request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        return Response(CategorySerializer(category, many=False, read_only=True).data)

    def create_category(self, request):
        parameters = self.generate_parameters(request)
        structured_category = CategoryDataStructure(**parameters)
        try:
            new_category = Category.objects.create(**structured_category.__dict__)
            new_category.save()
            return Response(CategorySerializer(new_category, many=False, read_only=True).data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex), "parameters": self.generate_parameters(request)},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def edit_category_id(self, request, category_id):
        parameters = self.generate_parameters(request)
        category = get_object_or_404(Category, id=category_id)
        return CategoryManager(category).edit(parameters)

    def edit_category_slug(self, request, category_slug):
        parameters = self.generate_parameters(request)
        category = get_object_or_404(Category, slug=category_slug)
        return CategoryManager(category).edit(parameters)

    @staticmethod
    def get_categories(request):
        print(request)
        categories = Category.objects.all()
        brand = request.GET.get('brand', False)
        print(brand)
        if brand:
            return Response(CategoryWithBrandSerializer(categories, many=True, read_only=True).data)
        else:
            return Response(CategorySerializer(categories, many=True, read_only=True).data)

    @staticmethod
    def delete_category_id(request, category_id):
        category = get_object_or_404(Category, id=category_id)
        return CategoryManager(category).delete()

    @staticmethod
    def delete_category_slug(request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        return CategoryManager(category).delete()

    @staticmethod
    def get_featured_categories(request):
        categories = Category.objects.filter(featured=True)
        return Response(CategorySerializer(categories, many=True, read_only=True).data)

    def get_permissions(self):
        if self.action == "create_category" or self.action == "edit_category_id" or self.action == "edit_category_slug" or self.action == "delete_category_id" or self.action == "delete_category_slug":
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super(CategoryAPI, self).get_permissions()


class CouponAPI(ViewSetBase):
    def validate(self, request):
        parameters = self.generate_parameters(request)
        code = parameters.get("code")
        if code:
            coupon = get_object_or_404(Coupon, code=code)
            return Response(CouponSerializer(coupon, many=False, read_only=True).data)
        else:
            return Response({"status": "failed", "message": "Code is required"}, status=status.HTTP_400_BAD_REQUEST)

    def create_coupon(self, request):
        parameters = self.generate_parameters(request)
        structured_coupon = CouponDataStructure(**parameters)
        try:
            new_coupon = Coupon.objects.create(**structured_coupon.__dict__)
            new_coupon.save()
            return Response(CouponSerializer(new_coupon, many=False, read_only=True).data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex), "parameters": self.generate_parameters(request)},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def edit_coupon(self, request, coupon_id):
        parameters = self.generate_parameters(request)
        structured_coupon = CouponDataStructure(**parameters)
        coupon = get_object_or_404(Coupon, id=coupon_id)
        try:
            coupon.__dict__.update(**structured_coupon.__dict__)
            coupon.save()
            return Response(CouponSerializer(coupon, many=False, read_only=True).data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex), "parameters": self.generate_parameters(request)},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def get_coupons(request):
        if request.user.is_staff or request.user.is_superuser:
            coupons = Coupon.objects.all()
            return Response(CouponSerializer(coupons, many=True, read_only=True).data)
        else:
            raise PermissionDenied

    def get_permissions(self):
        if self.action == "create_coupon" or self.action == "edit_coupon":
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super(CouponAPI, self).get_permissions()


class AddressAPI(ViewSetBase):
    @staticmethod
    def get_addresses(request):
        if request.user.is_superuser:
            addresses = Address.objects.all()
        else:
            addresses = Address.objects.filter(user=request.user)
        return Response(AddressSerializer(addresses, many=True, read_only=True).data)

    def create_address(self, request):
        parameters = self.generate_parameters(request)
        structured_address = AddressDataStructure(**parameters)
        newly_added_address = Address.objects.create(user=request.user, **structured_address.__dict__)
        newly_added_address.save()
        return Response(AddressSerializer(newly_added_address, many=False, read_only=True).data, status=status.HTTP_201_CREATED)

    def edit_address(self, request, address_id):
        parameters = self.generate_parameters(request)
        structured_address = AddressDataStructure(**parameters)
        address = get_object_or_404(Address, id=address_id)
        try:
            address.__dict__.update(**structured_address.__dict__)
            address.save()
            return Response(AddressSerializer(address, many=False, read_only=True).data, status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex), "parameters": self.generate_parameters(request)},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def delete_address(request, address_id):
        address = get_object_or_404(Address, id=address_id)
        try:
            address.delete()
            return Response({"status": "success", "message": "Address deleted"}, status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex)}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(AddressAPI, self).get_permissions()


class OrderAPI(ViewSetBase):

    @staticmethod
    def get_temporary_basket(request):
        temporary_basket = TemporaryBasket.objects.get_or_create(user=request.user)[0]
        return Response(TemporaryBasketSerializer(temporary_basket, many=False, read_only=True).data)

    def update_temporary_basket(self, request):
        parameters = self.generate_parameters(request)
        temporary_basket = TemporaryBasket.objects.get_or_create(user=request.user)[0]
        temporary_basket.data = parameters.get("data")
        temporary_basket.save()
        return Response(TemporaryBasketSerializer(temporary_basket, many=False, read_only=True).data)

    def submit_order(self, request):
        parameters = self.generate_parameters(request)
        address = get_object_or_404(Address, id=parameters.get("address"))
        products = parameters.get("products")
        coupon_code = parameters.get("coupon")
        coupon_object = get_object_or_404(Coupon, code=coupon_code) if coupon_code else None
        data = parameters.get('data')
        order = Order.objects.create(user=request.user, address=address, coupon=coupon_object, data=data)

        for product in products:
            product_id = product.get("product")
            quantity = product.get("quantity")
            product_object = get_object_or_404(Product, id=product_id)
            product_object.remaining -= quantity
            product_object.save()
            data = product.get('data')
            product_order = ProductOrder.objects.create(product=product_object, quantity=quantity, data=data, user=request.user)
            order.products.add(product_order)
        order.save()
        return Response(OrderSerializer(order, many=False, read_only=True).data)

    @staticmethod
    def get_orders(request):
        if request.user.is_superuser:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=request.user)
        return Response(OrderSerializer(orders, many=True, read_only=True).data)

    def edit_order(self, request, order_id):
        parameters = self.generate_parameters(request)
        order = get_object_or_404(Order, id=order_id)
        if parameters.get("address") is not None:
            address = get_object_or_404(Address, id=parameters.get("address"))
            order.address = address

        if parameters.get("coupon") is not None:
            coupon_code = parameters.get("coupon")
            coupon_object = get_object_or_404(Coupon, code=coupon_code) if coupon_code is not None else None
            order.coupon = coupon_object

        if parameters.get('data') is not None:
            data = parameters.get('data')
            order.data = data

        products = parameters.get("products")
        if products is not None:
            all_product_order_ids = [product_order.id for product_order in order.products.all()]
            for product in products:
                order_id = product.get("id")
                if order_id is not None:
                    all_product_order_ids.remove(order_id)
                product_id = product.get("product")
                product_object = get_object_or_404(Product, id=product_id)
                if order_id:
                    product_order = get_object_or_404(ProductOrder, id=order_id)
                    difference = product.get("quantity") - product_order.quantity
                    if difference > 0:
                        product_object.remaining -= difference
                        product_object.save()
                    elif difference < 0:
                        product_object.remaining += abs(difference)
                        product_object.save()

                    product_order.quantity = product.get("quantity")
                    product_order.data = product.get("data")
                    product_order.save()
                else:
                    product_object.remaining -= product.get("quantity")
                    product_order = ProductOrder.objects.create(product=product_object, quantity=product.get("quantity"), data=product.get("data"),
                                                                user=request.user)
                    product_object.save()
                    order.products.add(product_order)

            for product_order_id in all_product_order_ids:
                product_order = get_object_or_404(ProductOrder, id=product_order_id)
                order.products.remove(product_order)
                product_order.delete()

        order_status = parameters.get("status")
        if order_status is not None:
            order.status = order_status
        order.save()
        return Response(OrderSerializer(order, many=False, read_only=True).data)

    @staticmethod
    def delete_order(request, order_id):
        order = get_object_or_404(Order, id=order_id)
        try:
            for product_order in order.products.all():
                product_order.product.remaining += product_order.quantity
                product_order.product.save()
                product_order.delete()
            order.delete()
            return Response({"status": "success", "message": "Order deleted"}, status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex)}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(OrderAPI, self).get_permissions()


class CommentAPI(ViewSetBase):

    @staticmethod
    def get_comments(request, product_id):
        comments = Comment.objects.filter(product_id=product_id)
        return Response(CommentSerializer(comments, many=True, read_only=True).data)

    def create_comment(self, request, product_id):
        parameters = self.generate_parameters(request)
        product_object = get_object_or_404(Product, id=product_id)
        comment = Comment.objects.create(user=request.user, product=product_object, comment=parameters.get("comment"), rate=parameters.get("rate"),
                                         to=parameters.get("to"))
        return Response(CommentSerializer(comment, many=False, read_only=True).data)

    def edit_comment(self, request, comment_id):
        parameters = self.generate_parameters(request)
        comment = get_object_or_404(Comment, id=comment_id)
        comment.comment = parameters.get("comment")
        comment.rate = parameters.get("rate")
        comment.to = parameters.get("to")
        comment.save()
        return Response(CommentSerializer(comment, many=False, read_only=True).data)

    @staticmethod
    def delete_comment(request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        try:
            comment.delete()
            return Response({"status": "success", "message": "Comment deleted"}, status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex)}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(CommentAPI, self).get_permissions()


class FavoritView(ViewSetBase):
    @staticmethod
    def add_favorite(request, product_id):
        Favorit.objects.create(user=request.user, product_id=product_id)
        return Response(FavoritSerializer(Favorit.objects.filter(user=request.user), many=True).data)

    @staticmethod
    def remove_favorite(request, product_id):
        Favorit.objects.filter(user=request.user, product_id=product_id).delete()
        return Response(FavoritSerializer(Favorit.objects.filter(user=request.user), many=True).data)


class BrandAPI(ViewSetBase):

    @staticmethod
    def get_products(self, request, brand_id):
        parameters = self.generate_parameters(request)
        if parameters.get("category") is not None:
            products = Product.objects.filter(brand_id=brand_id, category_id=parameters.get("category"))
        else:
            products = Product.objects.filter(brand_id=brand_id)
        return Response(ProductSerializer(products, many=True, read_only=True).data)

    @staticmethod
    def get_brands(request):
        brands = Brand.objects.all()
        return Response(BrandSerializer(brands, many=True, read_only=True).data)

    def create_brand(self, request):
        parameters = self.generate_parameters(request)
        print(parameters)
        brand = BrandSerializer(data=parameters)
        if brand.is_valid():
            brand.save()
        else:
            return Response(brand.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(brand.data, status=status.HTTP_201_CREATED)

    def edit_brand(self, request, brand_id):
        parameters = self.generate_parameters(request)
        brand = get_object_or_404(Brand, id=brand_id)
        edited_brand = BrandSerializer(brand, data=parameters)
        if edited_brand.is_valid():
            edited_brand.save()
        else:
            return Response(edited_brand.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(BrandSerializer(brand, many=False, read_only=True).data, status=status.HTTP_202_ACCEPTED)

    @staticmethod
    def delete_brand(request, brand_id):
        brand = get_object_or_404(Brand, id=brand_id)
        try:
            brand.delete()
            return Response({"status": "success", "message": "Brand deleted"}, status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex)}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_permissions(self):
        if self.action == "get_brands":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated, IsAdminUser]

        return super(BrandAPI, self).get_permissions()
