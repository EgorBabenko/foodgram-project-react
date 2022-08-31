def set_ingredients_to_recipe(ingredients, recipe, RecipeIngredient):
    # print(type(data[0].get('id')))
    # print(data[0].get('amount'))
    for ingredient in ingredients:
        ingredient_to_recipe = ingredient.get('id')
        amount = ingredient.get('amount')
        RecipeIngredient.objects.create(recipe=recipe,
                                        ingredient=ingredient_to_recipe,
                                        amount=amount)
