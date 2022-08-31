from rest_framework import serializers
from recipes.serializers import ShortRecipeSerializer
from users.serializers import CustomUserSerializer
from users.models import CustomUser
from services.get_fields import get_recipes_count_field, get_user_recipes_field


class SubscribeSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes_count(self, obj):
        return get_recipes_count_field(obj)

    def get_recipes(self, obj):
        limit = self.context['request'].query_params.get('recipes_limit')
        return get_user_recipes_field(obj, ShortRecipeSerializer, limit)




