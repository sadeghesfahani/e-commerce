from django.contrib import admin
from store.models import Category, Order, Basket, Coupon, Product, Address

# Register your models here.
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Basket)
admin.site.register(Coupon)
admin.site.register(Product)
admin.site.register(Address)
