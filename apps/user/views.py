from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import render, redirect
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from apps.user.models import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.views import View

class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'auth/registration.html')

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        
        email = data.get('email')
        password = data.get('password')
        

        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response({"field": 'email', "message": "User doesn't exist."}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"field": 'password', "message": "Password doesn't match."}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with token generation
        serializer = self.serializer_class(context={"user": user})
        token_data = serializer.validate({})

        response_data = {
            'access': token_data['access'],
            'refresh': token_data['refresh'],
        }
        return Response(response_data, status=status.HTTP_200_OK)
    


class CustomTokenRefreshView(TokenRefreshView):
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        response_data = response.data

        return Response(response_data, status=status.HTTP_200_OK)
    

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')