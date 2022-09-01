from rest_framework import serializers
from services.get_fields import check_subscription

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        return check_subscription(self.context.get('request'), obj)


class AddCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        new_user = CustomUser(**validated_data)
        # обеспечение хеширования пароля
        new_user.set_password(new_user.password)
        new_user.save()
        # возврат "сырого" пароля для ответа апи
        new_user.password = validated_data.get('password')
        return new_user

