from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .models import User, PasswordResetCode
from .serializers import (
    UserSerializer,
    ForgotPasswordSerializer, VerifyResetCodeSerializer, ResetPasswordSerializer
)
import random
from drf_yasg.utils import swagger_auto_schema

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
class UsersMeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

def generate_code():
    return str(random.randint(100000, 999999))

class ForgotPasswordView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=ForgotPasswordSerializer,
        responses=({200: 'Reset code sent to email.', 404: 'User not found.'})
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        code = generate_code()
        PasswordResetCode.objects.create(user=user, code=code)
        send_mail(
            'Your Password Reset Code',
            f'Your code is: {code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=True,
        )
        return Response({'detail': 'Reset code sent to email.'})

class VerifyResetCodeView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=VerifyResetCodeSerializer,
        responses=({200: 'Code verified.', 400: 'Invalid code or email/Code expired.'})
    )
    def post(self, request):
        serializer = VerifyResetCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        try:
            user = User.objects.get(email=email)
            reset_code = PasswordResetCode.objects.filter(user=user, code=code, is_used=False).latest('created_at')
        except (User.DoesNotExist, PasswordResetCode.DoesNotExist):
            return Response({'detail': 'Invalid code or email.'}, status=status.HTTP_400_BAD_REQUEST)
        if reset_code.is_expired():
            return Response({'detail': 'Code expired.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Code verified.'})

class ResetPasswordView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        responses=({200: 'Password reset successful.', 400: 'Invalid code or email/Code expired.'})
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']
        try:
            user = User.objects.get(email=email)
            reset_code = PasswordResetCode.objects.filter(user=user, code=code, is_used=False).latest('created_at')
        except (User.DoesNotExist, PasswordResetCode.DoesNotExist):
            return Response({'detail': 'Invalid code or email.'}, status=status.HTTP_400_BAD_REQUEST)
        if reset_code.is_expired():
            return Response({'detail': 'Code expired.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        reset_code.is_used = True
        reset_code.save()
        return Response({'detail': 'Password reset successful.'})


