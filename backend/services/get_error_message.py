def get_error_message(error, name):
    """
    Генерация сообщения об ошибке
    Args:
        error (str): Имя исключения, например, IntegrityError.__str__
        name (str):  Имя модели, например, Favortie.__name__

    Returns:
        lambda() -> str : текст сообщения об ошибке
    """
    uniq = 'UNIQUE' in error
    repeat_sub = 'вы уже подписаны на этого пользователя'
    self_sub = 'нельзя подписаться на самого себя'
    repeat_fav = 'рецепт уже в избранном'
    repeat_shop = 'рецепт уже в списке покупок'
    answer_dict = {
        'Following': lambda: repeat_sub if uniq else self_sub,
        'Favorite': lambda: repeat_fav,
        'ShoppingCart': lambda: repeat_shop
    }

    return answer_dict[name]()
