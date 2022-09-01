def set_ingredients_to_recipe(ingredients, recipe, RecipeIngredient):
    RecipeIngredient.objects.bulk_create([
        RecipeIngredient(recipe=recipe,
                         ingredient=ingredient.get('id'),
                         amount=ingredient.get('amount'))
        for ingredient in ingredients
    ])
