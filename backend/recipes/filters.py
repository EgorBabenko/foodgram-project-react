from django_filters import rest_framework as basefilter

from .models import Ingredient, Recipe


class FilterForIngredients(basefilter.FilterSet):
    name = basefilter.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Ingredient
        fields = ('name', )


class FilterForRecipes(basefilter.FilterSet):
    is_favorited = basefilter.BooleanFilter(
        method='get_favorite',
        label='favorite'
    )
    is_in_shopping_cart = basefilter.BooleanFilter(
        method='get_is_in_shopping_cart',
        label='shopping_cart',
    )
    tags = basefilter.AllValuesMultipleFilter(
        field_name='tags__slug',
        label='tags',
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'is_favorited',
            'is_in_shopping_cart',
            'tags'
        )

    def get_favorite(self, queryset, name, value):
        if value:
            return queryset.filter(fans__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(byers__user=self.request.user)
        return queryset
