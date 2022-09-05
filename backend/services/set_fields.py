from recipes.models import RecipeIngredient


def set_ingredients_to_recipe(ingredients, recipe):
    """

    Args:
        ingredients (list): добавляемые ингредиенты
        recipe (recipes.models.Recipe): объект рецепта

    Returns:
        None
    """
    RecipeIngredient.objects.bulk_create([
        RecipeIngredient(recipe=recipe,
                         ingredient=ingredient.get('id'),
                         amount=ingredient.get('amount'))
        for ingredient in ingredients
    ])
