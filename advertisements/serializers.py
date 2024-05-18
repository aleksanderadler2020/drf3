import rest_framework.request
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('title', 'description', 'creator',
                  'status', 'created_at', )
        read_only_fields = ['creator', 'created_at', ]

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):

        if self.context["request"].method == 'POST' \
                and len(Advertisement.objects.filter(creator=self.context["request"].user,
                                                     status=AdvertisementStatusChoices.OPEN)) == 10:
            raise ValidationError("Максимальное кол-во открытых объявлений: 10")

        return data
