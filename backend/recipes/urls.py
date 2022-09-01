from django.urls import include, path
from recipes.models import Favorite, ShoppingCart
from rest_framework.routers import SimpleRouter

from .views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                    add_del_recipe_to_list)

router = SimpleRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('recipes/<int:pk>/favorite/',
         add_del_recipe_to_list,
         {'model': Favorite}),
    path(
        'recipes/<int:pk>/shopping_cart/',
        add_del_recipe_to_list,
        {'model': ShoppingCart}
    ),
    path('', include(router.urls)),
]
