from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Budget, Transaction
from .serializers import CategorySerializer, BudgetSerializer, TransactionSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class BudgetViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Budgets
    """
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['period_type', 'user']
    search_fields = ['period_type']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        # Set user and remaining_balance automatically
        amount = serializer.validated_data.get('amount', 0)
        serializer.save(user=self.request.user, remaining_balance=amount)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Transactions
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['transaction_type', 'category', 'user', 'date']
    search_fields = ['notes', 'category__name']
    ordering_fields = ['date', 'amount', 'created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    ordering = ['-date', '-created_at']