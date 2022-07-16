from rest_framework import viewsets


class ViewSetBase(viewsets.ViewSet):
    @staticmethod
    def generate_parameters(request):
        """
        this method is being used to combine all post, data and get parameters to make http method changes easier
        """
        get_dictionary = dict()
        for get_parameter in request.GET.keys():
            get_dictionary[get_parameter] = request.GET.get(get_parameter)
        return {**get_dictionary, **request.data}