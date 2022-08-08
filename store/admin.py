from django.contrib import admin
from store.models import Category, Order, ProductOrder, Coupon, Product, Address, Slider, Comment, Favorit,Brand

# Register your models here.
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(ProductOrder)
admin.site.register(Coupon)
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Slider)
admin.site.register(Comment)
admin.site.register(Favorit)
admin.site.register(Brand)
