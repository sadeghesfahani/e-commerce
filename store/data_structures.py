from django.shortcuts import get_object_or_404

from store.models import Category


class ProductDataStructure:
    def __init__(self, **kwargs):
        self._set_parameter("name", kwargs.get("name"))
        self._set_parameter("slug", kwargs.get("slug"))
        self._set_parameter("description", kwargs.get("description"))
        self._set_parameter("category", kwargs.get("category"))
        self._set_parameter("main_image", kwargs.get("mainImage"))
        self._set_parameter("images", kwargs.get("images"))
        self._set_parameter("attributes", kwargs.get("attributes"))
        self._set_parameter("options", kwargs.get("options"))
        self._set_parameter("extra_information", kwargs.get("extra_information"))
        self._set_parameter("remaining", kwargs.get("remaining"))

    def _set_parameter(self, parameter, value):
        if value is not None:
            if parameter == "category":
                self.category = get_object_or_404(Category, value)
            self.__dict__[parameter] = value
