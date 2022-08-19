from django.urls import path, re_path
# from .views import UserAPI

# from django.contrib.auth import views as auth_views
from user.views import UserAPI

urlpatterns = [
    path('register/', UserAPI.as_view({"post": "register"})),
    path('login/', UserAPI.as_view({"post": "login"}), name='login'),
    path('change_password/', UserAPI.as_view({"put": "change_password"}), name='change_password'),
    path('change_user_info/', UserAPI.as_view({"put": "change_user_info"}), name='change_user_info'),
    path('add_to_favorit/<int:product_id>', UserAPI.as_view({"get": "add_favorite", "delete": "remove_favorite"}), name='favorite'),
    path('get_all_users/', UserAPI.as_view({"get": "get_all_users"}), name='get_all_users'),


]
