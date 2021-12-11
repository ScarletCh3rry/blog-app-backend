from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenWithUsernameSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.login
        return token
