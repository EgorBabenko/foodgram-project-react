"""Модуль, обеспечивающий функционал валидации полей сериализаторов"""
from rest_framework.serializers import ValidationError


def check_cooking_time(value):
    """
    Проверка времени приготовления рецепта
    Args:
        value (int): время приготовления
    Raises:
         ValidationError: время приготовления не является положительным числом
    Returns:
        value(int)
    """
    if value <= 0:
        raise ValidationError('Время приготовления должно быть больше ноля')
    return value


def check_amount(value):
    """
    Проверка количества ингредиента
    Args:
        value (float): Количество ингредиента
    Raises:
         ValidationError: колечество не является положительным числом

    Returns:
        value (float)
    """
    if value <= 0:
        raise ValidationError('Количество ингредиента должно быть больше ноля')
    return value


def check_ingredients(ingredients):
    """
    Проверка ингредиентов на наличие, уникальность
    Args:
        ingredients (list): Список ингредиентов

    Returns:
        ingredients
    """
    if len(ingredients) == 0:
        raise ValidationError('Укажите ингредиенты')
    for ingredient in ingredients:
        check_amount(ingredient.get('amount'))
    names = [name['id'] for name in ingredients]
    if len(names) != len(set(names)):
        raise ValidationError('Ингредиенты не должны повторяться')

    return ingredients


def check_tags(tags):
    """
    Проверка тегов на наличие, уникальность
    Args:
        tags (list): Список тегов

    Returns:
        tags
    """
    if len(tags) == 0:
        raise ValidationError('Укажите теги!')
    if len(tags) != len(set(tags)):
        raise ValidationError('Не повторяйте теги!')
    return tags
