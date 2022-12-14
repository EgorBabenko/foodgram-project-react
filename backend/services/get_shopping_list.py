from django.db.models import F, Sum
from recipes.models import RecipeIngredient


def get_shopping_list(user):
    """
    Получение
    Args:
        user (users.models.CustomUser): объект пользователя

    Returns:
        ingredients (django.db.models.query.QuerySet): список ингредиентов + количество
    """
    ingredients = RecipeIngredient.objects.filter(
        recipe__byers__user=user).values(
        name=F('ingredient__name'),
        measurement_unit=F('ingredient__measurement_unit')
    ).annotate(amount=Sum('amount')).values_list(
        'ingredient__name', 'amount', 'ingredient__measurement_unit')
    return ingredients
