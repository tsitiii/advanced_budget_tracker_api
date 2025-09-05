from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from auth_feature.models import User

class Category(models.Model):
    """
    Model to store transaction categories (e.g., Food, Transport).
    Pre-defined categories can be seeded via a data migration or Django admin.
    """
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        

class Budget(models.Model):
    """
    Model to store a user's weekly or monthly budget.
    The remaining_balance is calculated automatically.
    """
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'
    PERIOD_CHOICES = [
        (PERIOD_WEEKLY, 'Weekly'),
        (PERIOD_MONTHLY, 'Monthly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='budgets' )
    period_type = models.CharField( max_length=10, choices=PERIOD_CHOICES,  default=PERIOD_WEEKLY )
    amount = models.DecimalField( max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))] )
    remaining_balance = models.DecimalField( max_digits=12, decimal_places=2, default=0.00)
    start_date = models.DateField( null=True,  blank=True,    help_text="The start date of this budget period (e.g., Monday for a week, 1st for a month).")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s {self.get_period_type_display()} Budget (${self.amount})"

    class Meta:
        constraints = [ models.UniqueConstraint(fields=['user', 'period_type', 'start_date'],    name='unique_budget_period'   ) ]
        ordering = ['-created_at']
        

class Transaction(models.Model):
    """
    Model to store a user's income or expense transactions.
    """
    TYPE_INCOME = 'income'
    TYPE_EXPENSE = 'expense'
    TRANSACTION_TYPE_CHOICES = [
        (TYPE_INCOME, 'Income'),
        (TYPE_EXPENSE, 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions' )
    
    category = models.ForeignKey( Category, on_delete=models.PROTECT,related_name='transactions' )
    
    transaction_type = models.CharField( max_length=10,    choices=TRANSACTION_TYPE_CHOICES)
    
    amount = models.DecimalField( max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))] )
    
    notes = models.TextField(blank=True, null=True)
    
    date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.transaction_type}: ${self.amount} on {self.date}"

    class Meta:
        ordering = ['-date', '-created_at']