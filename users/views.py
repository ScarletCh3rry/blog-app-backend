from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics

from users.models import CustomUser
from users.serializers import TokenWithUsernameSerializer, UserSerializer, RegisterSerializer, UserEditSerializer, \
    CustomTokenRefreshSerializer


class TokenWithUsernameObtainPairView(TokenObtainPairView):
    serializer_class = TokenWithUsernameSerializer


class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all().order_by('login')


class Register(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'login'


class UserProfileEditView(generics.UpdateAPIView):
    serializer_class = UserEditSerializer

    def get_object(self):
        if self.request.user.login != self.kwargs["login"]:
            raise PermissionDenied(detail="You can't change other profiles", code=None)
        return get_object_or_404(CustomUser.objects.all(), login=self.kwargs["login"])


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
