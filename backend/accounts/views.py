from django.shortcuts import render
from .serializers import UserSerializers, LoginSerializers
from rest_framework import generics, status
from rest_framework.views import APIView
# from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializers
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'User registered successfully',
                    'token': token.key,
                }, status=status.HTTP_201_CREATED)
            except:
                return Response({
                    'error': 'Username already exist'
                }, status=status.HTTP_400_BAD_REQUEST)
                
class LoginView(APIView):
    serializer_class = LoginSerializers
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializers(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.validated_data['user']
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'Your login',
                    'token': token.key,
                }, status=status.HTTP_200_OK)
            except:
                return Response({
                    'error': "User not found"
                }, status=status.HTTP_400_BAD_REQUEST)
                
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        try:
            token = Token.objects.get(user=user)
            token.delete()
            return Response({
                'message': 'Your logout'
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'error': "Can't logout at the moment"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        
            
                
