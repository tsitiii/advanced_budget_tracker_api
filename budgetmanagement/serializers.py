from rest_framework import serializers
from .models import Category, Budget, Transaction


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at', 'updated_at']


class BudgetSerializer(serializers.ModelSerializer):
    """Serializer for Budget model"""
    
    class Meta:
        model = Budget
        fields = [
            'id', 'user', 'period_type', 'amount', 'remaining_balance', 
            'start_date', 'created_at', 'updated_at'
        ]


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'user', 'category', 'category_name', 'transaction_type', 
            'amount', 'notes', 'date', 'created_at', 'updated_at'
        ]
