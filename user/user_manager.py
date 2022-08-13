from django.contrib.auth import authenticate
from .models import User
from exeptions.rest_framework_exeption import BadRequest
from django.http import Http404
from user.serializers import UserSerializer


class UserManager:

    def __init__(self, user=None):
        self.user = user

    def register(self, **kwargs):
        try:
            structured_data_for_user = UserDataStructure(**kwargs)
            new_user = User.objects.create_user(**structured_data_for_user.__dict__)
            new_user.set_password(structured_data_for_user.password)
            new_user.save()
            self.user = new_user
            return self.user
        except AttributeError:
            raise BadRequest

    def serialize(self):
        return UserSerializer(self.user, many=False).data

    @staticmethod
    def edit(**kwargs):
        structured_data_for_user = UserDataStructure(**kwargs)
        try:
            user = User.objects.get(username=structured_data_for_user.username)
            user.__dict__.update(**structured_data_for_user.__dict__)
            user.save()
        except AttributeError:
            raise BadRequest("username must specify")
        except User.DoesNotExist:
            raise Http404(f"username with username of {structured_data_for_user.username} does not exist")
        return user
    @staticmethod
    def login(request, *args, **kwargs):
        return authenticate(request=request, **kwargs)


class UserDataStructure:
    def __init__(self, username=None, password=None, email=None, phone=None, *args, **kwargs):
        self._set_parameter("username", username)
        self._set_parameter("password", password)
        self._set_parameter("email", email)
        self._set_parameter("phone", phone)
        self._set_parameter('first_name', kwargs.get('firstName'))
        self._set_parameter('last_name', kwargs.get('lastName'))

    def _set_parameter(self, parameter, value):
        if value is not None:
            self.__dict__[parameter] = value
