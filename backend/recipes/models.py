from django.db import models
from services.validate_fields import check_amount, check_cooking_time
from users.models import CustomUser

from .fields import HexField


class Tag(models.Model):
    name = models.CharField(max_length=20, blank=False,
                            unique=True, null=False,
                            verbose_name='Имя тега',
                            help_text='Введите имя тега')

    color = HexField(unique=True, blank=False, null=False,
                     verbose_name='HEX код цвета',
                     help_text='Введите HEX код цвета тега')

    slug = models.SlugField(blank=False, unique=True, null=False,
                            verbose_name='Slug тега',
                            help_text='Введите slug тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False,
                            verbose_name='Название ингредиента',
                            help_text='Введите название ингредиента')

    measurement_unit = models.CharField(max_length=12,
                                        blank=False, null=False,
                                        verbose_name='Единица измерения',
                                        help_text='Укажите единицу измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               blank=False, related_name='recipes', null=False,
                               verbose_name='Автор')
    name = models.CharField(max_length=32, blank=False, null=False,
                            verbose_name='Название')
    image = models.ImageField(null=True, blank=False,
                              verbose_name='Изображение')
    text = models.TextField(blank=False, null=False,
                            verbose_name='Текст рецепта')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         through_fields=('recipe',
                                                         'ingredient'),
                                         related_name='recipes',
                                         verbose_name='Ингредиенты рецепта',
                                         )
    tags = models.ManyToManyField(Tag, blank=False, verbose_name='Теги')
    cooking_time = models.PositiveIntegerField(blank=False, null=False,
                                               validators=[check_cooking_time],
                                               verbose_name='Время готовки')

    who_chose = models.ManyToManyField(CustomUser, through='Favorite',
                                       through_fields=('recipe', 'user'),
                                       related_name='favorites_recipes', )

    who_bought = models.ManyToManyField(CustomUser, through='ShoppingCart',
                                        through_fields=('recipe', 'user'),
                                        related_name='purchases_list', )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients_list',
                               on_delete=models.CASCADE,
                               verbose_name='рецепт')
    ingredient = models.ForeignKey(Ingredient,
                                   related_name='recipe_use',
                                   on_delete=models.CASCADE,
                                   verbose_name='тип ингредиента')
    amount = models.FloatField(blank=False, null=False,
                               verbose_name='количество',
                               validators=[check_amount])

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'
        constraints = [
            # ограничение повторного добавления ингредиента
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'], name='un'
            ), ]


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser,
                             related_name='favorites',
                             on_delete=models.CASCADE,
                             verbose_name='пользователь')
    recipe = models.ForeignKey(Recipe,
                               related_name='fans',
                               on_delete=models.CASCADE,
                               verbose_name='рецепт')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            # ограничение повторного добавления в избранное
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='un_fav'), ]

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser,
                             related_name='purchases',
                             on_delete=models.CASCADE,
                             verbose_name='пользователь')
    recipe = models.ForeignKey(Recipe,
                               related_name='byers',
                               on_delete=models.CASCADE,
                               verbose_name='рецепт')

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            # ограничение повторной покупки.
            models.UniqueConstraint(fields=['user', 'recipe'], name='uniq'), ]

    def __str__(self):
        return f'{self.recipe} в списке покупок у {self.user}'
