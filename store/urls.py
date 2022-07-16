from django.urls import path, re_path
from user.views import UserAPI

urlpatterns = [
    path('register/', UserAPI.as_view({"post": "register"})),


]
