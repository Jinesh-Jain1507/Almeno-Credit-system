from django.contrib import admin
from .models import Customer, Loan

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'first_name', 'last_name', 'phone_number', 'monthly_salary', 'approved_limit')
    search_fields = ('first_name', 'last_name', 'phone_number')
    list_filter = ('monthly_salary',)

# Register the Loan model
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('loan_id', 'customer', 'loan_amount', 'tenure', 'interest_rate')
    search_fields = ('customer__first_name', 'customer__last_name', 'loan_id')
    list_filter = ( 'tenure', 'interest_rate')