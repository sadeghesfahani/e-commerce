from django.urls import path, re_path
from store.views import ProductAPI, CategoryAPI

urlpatterns = [
    path('categories/', CategoryAPI.as_view({"get": "get_categories"})),
    path('category/', CategoryAPI.as_view({"post": "create_category"})),
    path('category/<int:category_id>', CategoryAPI.as_view({"put": "edit_category","delete":"delete_category"})),
    path('product/', ProductAPI.as_view({"post": "create_product", "get": "get_all_products"})),
    path('product/<int:product_id>', ProductAPI.as_view({"get": "get_product_by_id", "put": "edit_product","delete":"delete_product"})),
    path('product/category/<int:category_id>', ProductAPI.as_view({"get": "get_category_products"})),
]
