from django.db import IntegrityError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from foodgram.pagination import PageLimitPagination
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from services.get_error_message import get_error_message
from services.get_shopping_list import get_shopping_list
from weasyprint import HTML

from .filters import FilterForIngredients, FilterForRecipes
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import PermissionForRecipe
from .serializers import (AddRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, ShortRecipeSerializer,
                          TagSerializer)


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
def add_del_recipe_to_list(request, pk, model):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        try:
            model.objects.create(user=request.user, recipe=recipe)
            answer = ShortRecipeSerializer(recipe)
            return Response(answer.data, status=status.HTTP_201_CREATED
                            )
        except IntegrityError as error:
            error_message = get_error_message(error.__str__(),
                                              model.__name__)
            return Response({'errors': error_message},
                            status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if model.objects.filter(user=request.user, recipe=recipe).count() == 0:
            return Response({'errors': 'рецепта нет в списке'},
                            status=status.HTTP_400_BAD_REQUEST)
        obj = model.objects.get(user=request.user, recipe=recipe)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


