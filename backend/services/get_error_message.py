def get_error_message(error, name):
    uniq = 'UNIQUE' in error
    repeat_sub = 'вы уже подписаны на этого пользователя'
    self_sub = 'нельзя подписаться на самого себя'
    repeat_fav = 'рецепт уже в избранном'
    repeat_shop = 'рецепт уже в списке покупок'
    answer_dict = {
        'sub': lambda: repeat_sub if uniq else self_sub,
        'Favorite': lambda: repeat_fav,
        'ShoppingCart': lambda: repeat_shop
    }

    return answer_dict[name]()
