from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('token/', CustomTokenObtainPairView.as_view(), name='access_token'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='refresh_token'),
]
