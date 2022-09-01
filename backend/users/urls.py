from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

from .views import CustomUserViewSet

router = SimpleRouter()
router.register('users', CustomUserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken'))
]