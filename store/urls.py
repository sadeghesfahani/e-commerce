from django.urls import path, re_path
from store.views import ProductAPI, CategoryAPI

urlpatterns = [
    path('categories/', CategoryAPI.as_view({"get": "get_categories"})),
    path('category/', CategoryAPI.as_view({"post": "create_category"})),
    path('category/<int:category_id>', CategoryAPI.as_view({"put": "edit_category"})),
    path('product/', ProductAPI.as_view({"post": "create_product"})),
]
