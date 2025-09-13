from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsAuthenticated]
    """
    CRUD operations for Budgets
    """
    serializer_class = BudgetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['period_type']  # Remove 'user' from filterable fields
    search_fields = ['period_type']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        amount = serializer.validated_data.get('amount', 0)
        serializer.save(user=self.request.user, remaining_balance=amount)

    def perform_update(self, serializer):
        # Ensure user cannot change ownership
        serializer.save(user=self.request.user)

    def get_object(self):
        # Ensure users can only access their own budgets
        obj = super().get_object()
        if obj.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to access this budget.")
        return obj


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    """
    CRUD operations for Transactions
    """
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['transaction_type', 'category', 'date']  # Remove 'user' from filterable fields
    search_fields = ['notes', 'category__name']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date', '-created_at']

    def get_queryset(self):
        # Only return transactions belonging to the current user
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # Ensure user cannot change ownership
        serializer.save(user=self.request.user)

    def get_object(self):
        # Ensure users can only access their own transactions
        obj = super().get_object()
        if obj.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to access this transaction.")
        return obj