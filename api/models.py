from django.db import models
from datetime import datetime
from dateutil.relativedelta import relativedelta 

# Create your models here.

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null = True)
    age = models.IntegerField()
    monthly_salary = models.IntegerField()
    approved_limit = models.IntegerField()
    phone_number = models.CharField(max_length=15)

class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_amount = models.FloatField()
    tenure = models.IntegerField()
    interest_rate = models.FloatField()
    monthly_installment = models.FloatField()
    emis_paid_on_time = models.IntegerField()
    approved_date = models.DateField(default=datetime.now)
    end_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + relativedelta(months=self.tenure)
        super().save(*args, **kwargs)
