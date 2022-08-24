from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from store.data_structures import ProductDataStructure
from store.models import Category, Brand
from store.serializers import ProductSerializer


class ProductManager:
    def __init__(self, product):
        self.product = product

    def edit(self, parameters):
        structured_product = ProductDataStructure(**parameters)
        try:
            self.product.__dict__.update(**structured_product.__dict__)
            if structured_product.__dict__.get('category'):
                self.product.category = get_object_or_404(Category, id=structured_product.__dict__.get("category").id)
            if structured_product.__dict__.get('brand'):
                self.product.brand = get_object_or_404(Brand, id=structured_product.__dict__.get("brand").id)
            self.product.save()
            return Response(ProductSerializer(self.product, many=False, read_only=True).data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex), "parameters": parameters},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self):
        try:
            self.product.delete()
            return Response({"status": "success", "message": "Product deleted"}, status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex)}, status=status.HTTP_406_NOT_ACCEPTABLE)
