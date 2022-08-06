from rest_framework import serializers

from user.models import User, Favorit


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]


class FavoritSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorit
        fields = "__all__"
