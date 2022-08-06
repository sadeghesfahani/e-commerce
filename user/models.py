from django.db import models
from django.contrib.auth.models import AbstractUser
from e_commerce.store.models import Product

# Create your models here.
class User(AbstractUser):
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)


class Favorit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')