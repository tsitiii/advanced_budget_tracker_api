from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from decimal import Decimal
from .models import Transaction, Budget


@receiver([post_save, post_delete], sender=Transaction)
def update_budget_balance(sender, instance, **kwargs):
    """
    Update the remaining balance of the user's current budget when transactions change
    """
    user = instance.user
    
    # Get the user's most recent budget
    current_budget = Budget.objects.filter(user=user).first()
    
    if current_budget:
        # Calculate total expenses for this user
        total_expenses = Transaction.objects.filter(
            user=user,
            transaction_type='expense'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        # Calculate total income for this user
        total_income = Transaction.objects.filter(
            user=user,
            transaction_type='income'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        # Update remaining balance (budget amount - expenses + income)
        current_budget.remaining_balance = current_budget.amount - total_expenses + total_income
        current_budget.save(update_fields=['remaining_balance'])