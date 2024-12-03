from django.contrib import admin
from django.urls import path
from api.views import (
    RegisterCustomer,
    CheckEligibility,
    CreateLoan,
    ViewLoan,
    ViewLoans
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register', RegisterCustomer.as_view(), name='register-customer'),
    path('api/check-eligibility', CheckEligibility.as_view(), name='check-eligibility'),
    path('api/create-loan', CreateLoan.as_view(), name='create-loan'),
    path('api/view-loan/<int:loan_id>', ViewLoan.as_view(), name='view-loan'),
    path('api/view-loans/<int:customer_id>', ViewLoans.as_view(), name='view-loans'),
]
