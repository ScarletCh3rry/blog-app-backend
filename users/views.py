from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import TokenWithUsernameSerializer


class TokenWithUsernameObtainPairView(TokenObtainPairView):
    serializer_class = TokenWithUsernameSerializer
