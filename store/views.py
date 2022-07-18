from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from store.data_structures import ProductDataStructure, CategoryDataStructure, AddressDataStructure, CouponDataStructure
from store.models import Product, Category, TemporaryBasket, Coupon, Address, ProductOrder, Order
from store.serializers import ProductSerializer, CategorySerializer, TemporaryBasketSerializer, CouponSerializer, AddressSerializer, OrderSerializer
from store.viewset_base import ViewSetBase


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
    def delete_product(request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            return Response({"status": "success", "message": "Product deleted"}, status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex)}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def get_all_products(request):
        products = Product.objects.all()
        return Response(ProductSerializer(products, many=True, read_only=True).data)

    @staticmethod
    def get_category_products(request, category_id):
        if Category.objects.filter(id=category_id).exists():
            products = Product.objects.filter(category_id=category_id)
            return Response(ProductSerializer(products, many=True, read_only=True).data)
        else:
            raise Http404

    @staticmethod
    def get_product_by_id(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return Response(ProductSerializer(product, many=False, read_only=True).data)

    def edit_product(self, request, product_id):
        parameters = self.generate_parameters(request)
        structured_product = ProductDataStructure(**parameters)
        try:
            product = get_object_or_404(Product, id=product_id)
            product.__dict__.update(**structured_product.__dict__)
            if structured_product.__dict__.get('category'):
                product.category = get_object_or_404(Category, id=structured_product.__dict__.get("category").id)
            product.save()
            return Response(ProductSerializer(product, many=False, read_only=True).data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex), "parameters": self.generate_parameters(request)},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(ProductAPI, self).get_permissions()


class CategoryAPI(ViewSetBase):
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

    def edit_category(self, request, category_id):
        parameters = self.generate_parameters(request)
        structured_category = CategoryDataStructure(**parameters)
        category = get_object_or_404(Category, id=category_id)
        try:
            category.__dict__.update(**structured_category.__dict__)
            if structured_category.__dict__.get("parent"):
                category.parent = get_object_or_404(Category, id=structured_category.__dict__.get("parent").id)
            category.save()
            return Response(CategorySerializer(category, many=False, read_only=True).data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex), "parameters": self.generate_parameters(request)},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def get_categories(request):
        categories = Category.objects.all()
        return Response(CategorySerializer(categories, many=True, read_only=True).data)

    @staticmethod
    def delete_category(request, category_id):
        category = get_object_or_404(Category, id=category_id)
        try:
            category.delete()
            return Response({"status": "success", "message": "Category deleted"}, status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex)}, status=status.HTTP_406_NOT_ACCEPTABLE)


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


class AddressAPI(ViewSetBase):
    @staticmethod
    def get_addresses(request):
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
        orders = Order.objects.filter(user=request.user)
        return Response(OrderSerializer(orders, many=True, read_only=True).data)

    def edit_order(self, request, order_id):
        parameters = self.generate_parameters(request)
        order = get_object_or_404(Order, id=order_id)
        address = get_object_or_404(Address, id=parameters.get("address"))
        coupon_code = parameters.get("coupon")
        coupon_object = get_object_or_404(Coupon, code=coupon_code) if coupon_code is not None else None
        data = parameters.get('data')
        order.address = address
        order.coupon = coupon_object
        order.data = data
        products = parameters.get("products")
        order_status = parameters.get("status")
        order.status = order_status
        print("here")
        for product in products:
            order_id = product.get("id")
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
