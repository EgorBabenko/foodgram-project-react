from django.urls import path

from .views import SubscriptionsAPIView, add_or_delete_sub

urlpatterns = [
    path('users/subscriptions/', SubscriptionsAPIView.as_view()),
    path('users/<int:pk>/subscribe/', add_or_delete_sub)
]