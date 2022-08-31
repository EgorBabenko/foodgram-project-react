from django.contrib import admin
from .models import (Tag, Recipe, Ingredient, RecipeIngredient, Favorite,
                     ShoppingCart, RecipeIngredient)


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    fk_name = 'recipe'
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInLine, )
    list_display = ('author', 'name',)
    readonly_fields = ('favorited',)
    list_filter = ('name', 'author', 'tags',)
    filter_horizontal = ('tags',)
    list_display_links = ('name', )

    def favorited(self, obj):
        return obj.who_chose.all().count()

    favorited.short_description = 'Количество добавлений в избранное'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_display_links = ('name', )
    list_filter = ('name', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name', )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_display_links = ('user', )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display =('user', 'recipe')
    list_display_links = ('user', )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    list_display_links = ('recipe', 'ingredient')




