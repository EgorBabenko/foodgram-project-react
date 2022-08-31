import re
from django.db import IntegrityError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .permissions import PermissionForRecipe
from rest_framework.permissions import SAFE_METHODS
from services.get_error_message import get_error_message
from services.get_shopping_list import get_shopping_list
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer, ShortRecipeSerializer,
                          AddRecipeSerializer)
from .filters import FilterForIngredients, FilterForRecipes
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from .models import Tag, Ingredient, Recipe, Favorite, ShoppingCart
from foodgram.pagination import PageLimitPagination
from weasyprint import HTML


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterForIngredients


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageLimitPagination
    permission_classes = (PermissionForRecipe, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterForRecipes

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return AddRecipeSerializer


    @action(detail=False)
    def download_shopping_cart(self, request):
        ingredients = get_shopping_list(request.user)
        html_template = render_to_string('recipes/template_for_pdf.html',
                                         {'ingredients': ingredients})
        html = HTML(string=html_template)
        result = html.write_pdf()
        response = HttpResponse(result, content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; filename=shopping_list.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        return response


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def add_del_recipe_to_list(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if re.match(r'^/api/recipes/\d{1,}/favorite/$', request.path):
        model = Favorite
        name = 'favorite'
        related_manager = recipe.who_chose

    elif re.match(r'^/api/recipes/\d{1,}/shopping_cart/$', request.path):
        model = ShoppingCart
        name = 'shopping'
        related_manager = recipe.who_bought

    if request.method == 'POST':
        try:
            model.objects.create(user=request.user, recipe=recipe)
            answer = ShortRecipeSerializer(recipe)
            return Response(answer.data, status=status.HTTP_201_CREATED
                            )
        except IntegrityError as error:
            error_message = get_error_message(error.__str__(),
                                              name)
            return Response({'errors': error_message},
                            status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if request.user not in related_manager.all():
            return Response({'errors': 'рецепта нет в списке'},
                            status=status.HTTP_400_BAD_REQUEST)
        obj = model.objects.get(user=request.user, recipe=recipe)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


