from django.contrib import admin
from .models import Expense

class ExpenseAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('user', 'amount', 'description', 'split_method', 'created_at')

    # Filters for the right sidebar
    list_filter = ('split_method', 'created_at', 'user')

    # Search bar for searching expenses by description and user
    search_fields = ('description', 'user__email')

    # Fieldsets to organize the detail view
    fieldsets = (
        (None, {
            'fields': ('user', 'amount', 'description', 'split_method', 'participants')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('created_at',),
        }),
    )

    # Makes 'created_at' field read-only
    readonly_fields = ('created_at',)

# Register the Expense model with the custom admin configuration
admin.site.register(Expense, ExpenseAdmin)
