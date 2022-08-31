from rest_framework.routers import SimpleRouter

from django.urls import path, include
from .views import (TagViewSet, IngredientViewSet,
                    RecipeViewSet, add_del_recipe_to_list)

router = SimpleRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('recipes/<int:pk>/favorite/', add_del_recipe_to_list),
    path('recipes/<int:pk>/shopping_cart/', add_del_recipe_to_list),
    path('', include(router.urls)),
]
