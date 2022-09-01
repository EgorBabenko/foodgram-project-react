from rest_framework.serializers import ValidationError


def check_cooking_time(value):
    if value <= 0:
        raise ValidationError('Время приготовления должно быть больше ноля')
    return value

def check_amount(value):
    if value <= 0:
        raise ValidationError('Количество ингредиента должно быть больше ноля')
    return value


def check_ingredients(ingredients):
    if len(ingredients) == 0:
        raise ValidationError('Укажите ингредиенты')
    for ingredient in ingredients:
        check_amount(ingredient.get('amount'))
    names = [name['id'] for name in ingredients]
    if len(names) != len(set(names)):
        raise ValidationError('Ингредиенты не должны повторяться')

    return ingredients


def check_tags(tags):
    if len(tags) == 0:
        raise ValidationError('Укажите теги!')
    if len(tags) != len(set(tags)):
        raise ValidationError('Не повторяйте теги!')
    return tags


