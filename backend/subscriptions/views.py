from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from services.get_error_message import get_error_message
from users.models import CustomUser, Following

from .serializers import SubscribeSerializer


class SubscriptionsAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return self.request.user.sub_list.all()


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def add_or_delete_sub(request, pk):
    leader = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        try:
            Following.objects.create(follower=request.user, leader=leader)
            context = {'request': request}
            leader = SubscribeSerializer(leader, context=context)
            return Response(leader.data, status=status.HTTP_201_CREATED
                            )
        except IntegrityError as error:
            error_message = get_error_message(error.__str__(),
                                              Following.__name__)
            return Response({'errors': error_message},
                            status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if leader not in request.user.sub_list.all():
            return Response(
                {
                    'errors': 'вы не были подписаны на этого пользователя',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        follow = Following.objects.get(follower=request.user, leader=leader)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


