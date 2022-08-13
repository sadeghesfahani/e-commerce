from django.db import models

# Create your models here.
from user.models import User


class Slider(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=100000, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True)
    image = models.CharField(max_length=25000, null=True, blank=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=25000, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    final_price = models.DecimalField(max_digits=20, decimal_places=2)
    main_image = models.CharField(max_length=25000, null=True, blank=True)
    images = models.JSONField(blank=True, null=True)
    attributes = models.JSONField(blank=True, null=True)
    options = models.JSONField(blank=True, null=True)
    extra_information = models.JSONField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    remaining = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    related_products = models.ManyToManyField('self', blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Coupon(models.Model):
    code = models.CharField(max_length=100, unique=True)
    discount = models.DecimalField(max_digits=20, decimal_places=2)
    discount_type = models.CharField(max_length=100)  # percent or amount
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class ProductOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    data = models.JSONField(blank=True, null=True)
    quantity = models.SmallIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_address")
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100)
    coordinates = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductOrder)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='pending')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def total(self):
        total = 0
        for product in self.products.all():
            total += product.product.final_price * product.quantity

        if self.coupon:
            if self.coupon.discount_type == 'percent':
                total = total - (total * self.coupon.discount / 100)
            else:
                total = total - self.coupon.discount
        return total


class TemporaryBasket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.JSONField(blank=True, null=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    rate = models.SmallIntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    to = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='replies')
    like = models.ManyToManyField(User, blank=True, related_name='like_comment')
    dislike = models.ManyToManyField(User, blank=True, related_name='dislike_comment')

    def __str__(self):
        return self.user.username


class Favorit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')
