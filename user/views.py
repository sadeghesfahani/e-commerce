from django.contrib.auth import authenticate
from django.http import Http404
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status

from user.models import User
from user.serializers import UserSerializer
from user.user_manager import UserManager
from rest_framework.authtoken.models import Token


class UserAPI(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]

    def register(self, request):
        try:
            new_user = UserManager().register(**self.generate_parameters(request))
            token, _ = Token.objects.get_or_create(user=new_user)
            return Response({**UserSerializer(new_user, many=False, read_only=True).data, "token": token.key}, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex), "parameters": self.generate_parameters(request)},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def login(self, request):
        user = UserManager().login(request, **self.generate_parameters(request))
        if user is None:
            return Response({"status": "failed"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            token, _ = Token.objects.get_or_create(user=user)
            user_information = {"userInfo": UserSerializer(user, many=False, read_only=True).data, "token": token.key}
            return Response(user_information)

    def change_password(self, request):
        parameters = self.generate_parameters(request)
        username = parameters.get("username")
        old_password = parameters.get("oldPassword")
        new_password = parameters.get("newPassword")
        user = authenticate(request=request, username=username, password=old_password)
        if user is None:
            return Response({"status": "failed", "message": "old password is incorrect"}, status=status.HTTP_403_FORBIDDEN)
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        return Response({"status": "done"})

    def change_user_info(self, request):
        parameters = self.generate_parameters(request)
        user = request.user
        if user.is_superuser and parameters.get("username") is not None:
            username = parameters.get("username")
            user = User.objects.get(username=username)
            user_manager = UserManager(user)
            user_manager.edit(**parameters)
            return Response(UserSerializer(user, many=False, read_only=True).data)

        else:
            user_manager = UserManager(user)
            user = user_manager.edit(**parameters, username=user.username)
            return Response(UserSerializer(user, many=False, read_only=True).data)

    @staticmethod
    def get_all_users(request):
        if not request.user.is_superuser:
            raise PermissionDenied
        users = User.objects.all()
        return Response(UserSerializer(users, many=True, read_only=True).data)

    @staticmethod
    def generate_parameters(request):
        """
        this method is being used to combine all post, data and get parameters to make http method changes easier
        """
        get_dictionary = dict()
        for get_parameter in request.GET.keys():
            get_dictionary[get_parameter] = request.GET.get(get_parameter)
        return {**get_dictionary, **request.data}
