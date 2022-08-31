def check_subscription(request, obj):
    if request.user.is_authenticated:
        return obj in request.user.sub_list.all()
    return False


def get_recipe_ingredient_list(obj, serializer):
    queryset = obj.ingredients_list.all()
    serializer_obj = serializer(queryset, many=True)
    return serializer_obj.data


def get_is_favorited_field(request, obj):
    if request.user.is_authenticated:
        return obj in request.user.favorites_recipes.all()
    return False


def get_is_in_shopping_cart_field(request, obj):
    if request.user.is_authenticated:
        return obj in request.user.purchases_list.all()
    return False


def get_recipes_count_field(obj):
    return obj.recipes.count()


def get_user_recipes_field(obj, serializer, limit):
    if limit:
        limit = int(limit)
        queryset = obj.recipes.all()[:limit]
    else:
        queryset = obj.recipes.all()
    serializer_obj = serializer(queryset, many=True)
    return serializer_obj.data

