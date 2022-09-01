from recipes.serializers import ShortRecipeSerializer
from rest_framework import serializers
from services.get_fields import get_user_recipes_field
from users.models import CustomUser
from users.serializers import CustomUserSerializer


class SubscribeSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(source='recipes.count')

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes(self, obj):
        limit = self.context['request'].query_params.get('recipes_limit')
        return get_user_recipes_field(obj, ShortRecipeSerializer, limit)




