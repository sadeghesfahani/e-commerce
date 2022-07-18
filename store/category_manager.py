from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from store.data_structures import CategoryDataStructure
from store.models import Category
from store.serializers import CategorySerializer


class CategoryManager:
    def __init__(self, category):
        self.category = category

    def edit(self, parameters):
        structured_category = CategoryDataStructure(**parameters)
        try:
            self.category.__dict__.update(**structured_category.__dict__)
            if structured_category.__dict__.get("parent"):
                self.category.parent = get_object_or_404(Category, id=structured_category.__dict__.get("parent").id)
            self.category.save()
            return Response(CategorySerializer(self.category, many=False, read_only=True).data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex), "parameters": parameters},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self):
        try:
            self.category.delete()
            return Response({"status": "success", "message": "Category deleted"}, status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex)}, status=status.HTTP_406_NOT_ACCEPTABLE)