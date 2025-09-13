from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BudgetViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'budgets', BudgetViewSet, basename='budgets')
router.register(r'transactions', TransactionViewSet , basename='transactions')

urlpatterns = [
    path('v1/', include(router.urls)),
]
