"""
Модуль обеспечивает функционал получения значений полей для сериализаторов
"""


def check_subscription(request, obj):
    """
    Проверка факта подписки на получаемого пользователя
    Args:
        request (rest_framework.request.Request): объект запроса
        obj (users.models.CustomUser): объект запрашиваемого пользователя

    Returns:
        bool
    """
    if request.user.is_authenticated:
        return obj in request.user.sub_list.all()
    return False


def get_recipe_ingredient_list(obj, serializer):
    """
    Получение данных сериализации ингредиентов конкретного рецепта
    Args:
        obj (recipes.models.Recipe): объект рецепта
        serializer (recipes.serializers.RecipeIngredientSerializer): сериализатор

    Returns:
        serializer_obj.data (dict): данные сериализации
    """
    queryset = obj.ingredients_list.all()
    serializer_obj = serializer(queryset, many=True)
    return serializer_obj.data


def get_is_favorited_field(request, obj):
    """
    Проверка наличия рецепта в списке избранного
    Args:
        request (rest_framework.request.Request): объект запроса
        obj (recipes.models.Recipe): объект рецепта

    Returns:
        bool
    """
    if request.user.is_authenticated:
        return obj in request.user.favorites_recipes.all()
    return False


def get_is_in_shopping_cart_field(request, obj):
    """
    Проверка наличия рецепта в списке покупок
    Args:
        request (rest_framework.request.Request): объект запроса
        obj (recipes.models.Recipe): объект рецепта
    Returns:
        bool
    """
    if request.user.is_authenticated:
        return obj in request.user.purchases_list.all()
    return False


def get_user_recipes_field(obj, serializer, limit):
    """
    Получение данных сериализации рецептов конкретного пользователя
    Args:
        obj (users.models.CustomUser): объект пользователя
        serializer (recipes.serializers.ShortRecipeSerializer): сериализатор
        limit (int): лимит рецептов для сериализации

    Returns:
        serializer_obj.data (dict): данные сериализации
    """
    if limit:
        limit = int(limit)
        queryset = obj.recipes.all()[:limit]
    else:
        queryset = obj.recipes.all()
    serializer_obj = serializer(queryset, many=True)
    return serializer_obj.data
