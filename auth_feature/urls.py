from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ForgotPasswordView, VerifyResetCodeView, ResetPasswordView, UsersMeView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('api/v1/users/me',UsersMeView.as_view(),name='me'),
    path('api/v1/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('api/v1/verify-reset-code/', VerifyResetCodeView.as_view(), name='verify_reset_code'),
    path('api/v1/reset-password/', ResetPasswordView.as_view(), name='reset_password'),
]
