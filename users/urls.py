from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import TokenWithUsernameObtainPairView, UserView, Register, UserProfileView, UserProfileEditView, \
    CustomTokenRefreshView

urlpatterns = [
    path('token/', TokenWithUsernameObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserView.as_view()),
    path('register/', Register.as_view()),
    path('user-profile/<str:login>/', UserProfileView.as_view()),
    path('user-profile/<str:login>/edit/', UserProfileEditView.as_view())
]
