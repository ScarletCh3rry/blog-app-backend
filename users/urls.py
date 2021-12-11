from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import TokenWithUsernameObtainPairView

urlpatterns = [
    path('token/', TokenWithUsernameObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]