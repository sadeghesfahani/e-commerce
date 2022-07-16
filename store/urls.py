from django.urls import path, re_path
from store.views import ProductAPI, CategoryAPI

urlpatterns = [
    path('categories/', CategoryAPI.as_view({"get": "get_categories"})),

]
