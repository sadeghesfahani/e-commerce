from django.urls import path, re_path
from store.views import ProductAPI, CategoryAPI, CouponAPI, OrderAPI, AddressAPI

urlpatterns = [
    path('category/', CategoryAPI.as_view({"post": "create_category", "get": "get_categories"})),
    path('category/id/<int:category_id>', CategoryAPI.as_view({"put": "edit_category_id", "delete": "delete_category_id"})),
    path('category/slug/<slug:category_slug>', CategoryAPI.as_view({"put": "edit_category_slug", "delete": "delete_category_slug"})),
    path('product/', ProductAPI.as_view({"post": "create_product", "get": "get_all_products"})),
    path('product/id/<int:product_id>', ProductAPI.as_view({"get": "get_product_by_id", "put": "edit_product_id", "delete": "delete_product_id"})),
    path('product/slug/<slug:product_slug>',
         ProductAPI.as_view({"get": "get_product_by_slug", "put": "edit_product_slug", "delete": "delete_product_slug"})),
    path('product/featured', ProductAPI.as_view({"get": "create_featured_product"})),
    path('product/category/id/<int:category_id>', ProductAPI.as_view({"get": "get_category_products_id"})),
    path('product/category/slug/<slug:category_slug>', ProductAPI.as_view({"get": "get_category_products_slug"})),
    path('product/search/', ProductAPI.as_view({"get": "search"})),
    path('coupon', CouponAPI.as_view({"get": "get_coupons", "post": "create_coupon"})),
    path('coupon/validate', CouponAPI.as_view({"post": "validate"})),
    path('coupon/<int:coupon_id>', CouponAPI.as_view({"put": "edit_coupon"})),
    path('address/', AddressAPI.as_view({"get": "get_addresses", "post": "create_address"})),
    path('address/<int:address_id>', AddressAPI.as_view({"put": "edit_address", "delete": "delete_address"})),
    path('temporary_basket', OrderAPI.as_view({"get": "get_temporary_basket", "put": "update_temporary_basket"})),
    path('order', OrderAPI.as_view({"post": "submit_order", "get": "get_orders"})),
    path('order/<int:order_id>', OrderAPI.as_view({"put": "edit_order", "delete": "delete_order"})),
]
