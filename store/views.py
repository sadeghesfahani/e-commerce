from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from store.data_structures import ProductDataStructure
from store.models import Product
from store.serializers import ProductSerializer


class ProductAPI(viewsets.ViewSet):

    def create_product(self, request):
        parameters = self.generate_parameters(request)
        structured_product = ProductDataStructure(**parameters)
        new_product = Product.objects.create(**structured_product.__dict__)
        new_product.save()
        return Response(ProductSerializer(new_product, many=False, read_only=True).data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(ProductAPI, self).get_permissions()

    @staticmethod
    def generate_parameters(request):
        """
        this method is being used to combine all post, data and get parameters to make http method changes easier
        """
        get_dictionary = dict()
        for get_parameter in request.GET.keys():
            get_dictionary[get_parameter] = request.GET.get(get_parameter)
        return {**get_dictionary, **request.data}
