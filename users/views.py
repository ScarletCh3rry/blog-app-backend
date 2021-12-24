from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

from users.models import CustomUser
from users.serializers import TokenWithUsernameSerializer, UserSerializer, RegisterSerializer


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
