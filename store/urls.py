from django.urls import path, re_path
from store.views import ProductAPI, CategoryAPI, CouponAPI, OrderAPI, AddressAPI

urlpatterns = [
    path('categories/', CategoryAPI.as_view({"get": "get_categories"})),
    path('category/', CategoryAPI.as_view({"post": "create_category"})),
    path('category/<int:category_id>', CategoryAPI.as_view({"put": "edit_category", "delete": "delete_category"})),
    path('product/', ProductAPI.as_view({"post": "create_product", "get": "get_all_products"})),
    path('product/<int:product_id>', ProductAPI.as_view({"get": "get_product_by_id", "put": "edit_product", "delete": "delete_product"})),
    path('product/category/<int:category_id>', ProductAPI.as_view({"get": "get_category_products"})),
    path('coupon', CouponAPI.as_view({"get": "get_coupons", "post": "create_coupon"})),
    path('coupon/validate', CouponAPI.as_view({"post": "validate"})),
    path('coupon/<int:coupon_id>', CouponAPI.as_view({"put": "edit_coupon"})),
    path('address/', AddressAPI.as_view({"get": "get_addresses", "post": "create_address"})),
    path('address/<int:address_id>', AddressAPI.as_view({"put": "edit_address", "delete": "delete_address"})),
    path('temporary_basket', OrderAPI.as_view({"get": "get_temporary_basket", "put": "update_temporary_basket"})),
]
