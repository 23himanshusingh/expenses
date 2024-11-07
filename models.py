from django.db import models
from django.conf import settings

class Expense(models.Model):
    SPLIT_METHODS = [
        ('equal', 'Equal'),
        ('exact', 'Exact'),
        ('percentage', 'Percentage'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    split_method = models.CharField(max_length=10, choices=SPLIT_METHODS)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_expenses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.description} - {self.amount} ({self.split_method})'
