from rest_framework import status
from rest_framework.permissions import BasePermission


class OnlyOwnPost(BasePermission):
    def has_permission(self, request, view):
        return request.user.login == request.parser_context['kwargs']['login']

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Нельзя создавать опрос у чужого поста'