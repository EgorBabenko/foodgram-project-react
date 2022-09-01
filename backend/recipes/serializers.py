from rest_framework import serializers
from services.get_fields import (get_is_favorited_field,
                                 get_is_in_shopping_cart_field,
                                 get_recipe_ingredient_list)
from services.set_fields import set_ingredients_to_recipe
from services.validate_fields import (check_cooking_time, check_ingredients,
                                      check_tags)
from users.serializers import CustomUserSerializer

from .fields import Base64ImageField
from .models import Ingredient, Recipe, RecipeIngredient, Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор тегов
    """

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор типа ингредиента
    """

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор ингредиента в рецепте
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода полной версии рецепта
    """
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_ingredients(self, obj):
        return get_recipe_ingredient_list(obj, RecipeIngredientSerializer)

    def get_is_favorited(self, obj):
        return get_is_favorited_field(self.context.get('request'), obj)

    def get_is_in_shopping_cart(self, obj):
        return get_is_in_shopping_cart_field(self.context.get('request'), obj)


class ShortRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для краткой формы рецепта (подписки, избранное, покупки)
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class AddIngredientsToRecipe(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.FloatField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class AddRecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    ingredients = AddIngredientsToRecipe(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'text', 'image', 'cooking_time')

    def validate(self, data):
        check_ingredients(data.get('ingredients'))
        check_tags(data.get('tags'))
        check_cooking_time(data.get('cooking_time'))
        return data

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        set_ingredients_to_recipe(ingredients, recipe, RecipeIngredient)
        recipe.tags.set(tags)
        return recipe

    def update(self, recipe, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        set_ingredients_to_recipe(ingredients, recipe, RecipeIngredient)
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)

    def to_representation(self, recipe):
        data = RecipeSerializer(
            recipe,
            context={'request': self.context.get('request')}).data
        return data
