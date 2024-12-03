from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Loan, Customer
from datetime import datetime

# Create your views here.

class RegisterCustomer(APIView):
    def post(self, request):
        data = request.data
        monthly_salary = data.get('monthly_income')
        approved_limit = round(36 * monthly_salary, -5)
        
        customer = Customer.objects.create(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            age=data.get('age'),
            monthly_salary=monthly_salary,
            approved_limit=approved_limit,
            phone_number=data.get('phone_number'),
        )
        response_data = {
            "customer_id": customer.customer_id,
            "name": f"{customer.first_name} {customer.last_name}",
            "age": customer.age,
            "monthly_income": customer.monthly_salary,
            "approved_limit": customer.approved_limit,
            "phone_number": customer.phone_number,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class CheckEligibility(APIView):
    def post(self, request):
        data = request.data
        customer_id = data.get('customer_id')
        loan_amount = data.get('loan_amount')
        interest_rate = data.get('interest_rate')
        tenure = data.get('tenure')

        try:
            customer = Customer.objects.get(customer_id=customer_id)
            current_loans = Loan.objects.filter(customer=customer, approved=True)
            current_debt = sum(loan.loan_amount for loan in current_loans)

            if current_debt > customer.approved_limit:
                return Response({"credit_score": 0, "approval": False}, status=status.HTTP_200_OK)

            credit_score = 100 - len(current_loans) * 10
            if credit_score > 50:
                corrected_interest_rate = interest_rate
            elif 30 < credit_score <= 50:
                corrected_interest_rate = max(interest_rate, 12)
            elif 10 < credit_score <= 30:
                corrected_interest_rate = max(interest_rate, 16)
            else:
                return Response({"approval": False, "credit_score": credit_score}, status=status.HTTP_200_OK)

            monthly_installment = (loan_amount * (1 + corrected_interest_rate / 100)) / tenure
            response_data = {
                "customer_id": customer_id,
                "approval": True,
                "interest_rate": interest_rate,
                "corrected_interest_rate": corrected_interest_rate,
                "tenure": tenure,
                "monthly_installment": monthly_installment,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        
class CreateLoan(APIView):
    def post(self, request):
        data = request.data
        customer_id = data.get('customer_id')
        loan_amount = data.get('loan_amount')
        interest_rate = data.get('interest_rate')
        tenure = data.get('tenure')

        try:
            customer = Customer.objects.get(customer_id=customer_id)
            if loan_amount + customer.approved_limit > customer.approved_limit:
                return Response({"loan_approved": False, "message": "Loan exceeds limit"}, status=status.HTTP_400_BAD_REQUEST)

            monthly_installment = (loan_amount * (1 + interest_rate / 100)) / tenure
            loan = Loan.objects.create(
                customer=customer,
                loan_amount=loan_amount,
                interest_rate=interest_rate,
                tenure=tenure,
                monthly_installment=monthly_installment,
                emis_paid_on_time=0,
            )

            response_data = {
                "loan_id": loan.loan_id,
                "customer_id": customer.customer_id,
                "loan_approved": True,
                "monthly_installment": loan.monthly_installment,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

class ViewLoan(APIView):
    def get(self, request, loan_id):
        try:
            loan = Loan.objects.get(loan_id=loan_id)
            customer = loan.customer
            response_data = {
                "loan_id": loan.loan_id,
                "customer": {
                    "id": customer.customer_id,
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "phone_number": customer.phone_number,
                    "age": customer.age,
                },
                "loan_amount": loan.loan_amount,
                "interest_rate": loan.interest_rate,
                "monthly_installment": loan.monthly_installment,
                "tenure": loan.tenure,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)

class ViewLoans(APIView):
    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(customer_id=customer_id)
            loans = Loan.objects.filter(customer=customer, approved=True)
            response_data = [
                {
                    "loan_id": loan.loan_id,
                    "loan_amount": loan.loan_amount,
                    "interest_rate": loan.interest_rate,
                    "monthly_installment": loan.monthly_installment,
                    "repayments_left": loan.tenure - loan.emis_paid_on_time,
                }
                for loan in loans
            ]
            return Response(response_data, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
