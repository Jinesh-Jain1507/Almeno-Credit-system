import pandas as pd

def load_customer_data(apps, schema_editor):
    customer_file = "data/customer_data.xlsx"
    Customer = apps.get_model('api', 'Customer')
    df = pd.read_excel(customer_file)

    for _, row in df.iterrows():
        if not Customer.objects.filter(customer_id=row['Customer ID']).exists():
            Customer.objects.create(
                customer_id=row['Customer ID'],
                first_name=row['First Name'],
                last_name=row['Last Name'],
                age=row['Age'],
                phone_number=row['Phone Number'],
                monthly_salary=row['Monthly Salary'],
                approved_limit=row['Approved Limit'],
            )
    print("Customer data loaded successfully!")


def load_loan_data(apps, schema_editor):
    loan_file = "data/loan_data.xlsx"
    Loan = apps.get_model('api', 'Loan')
    Customer = apps.get_model('api', 'Customer')

    # Read the Excel file using pandas
    df = pd.read_excel(loan_file)

    for _, row in df.iterrows():
        try:
            customer = Customer.objects.get(customer_id=row['Customer ID'])
            if not Loan.objects.filter(loan_id=row['Loan ID']).exists():
                Loan.objects.create(
                    customer=customer,
                    loan_id=row['Loan ID'],
                    loan_amount=row['Loan Amount'],
                    tenure=row['Tenure'],
                    interest_rate=row['Interest Rate'],
                    monthly_installment=row['Monthly payment'],
                    emis_paid_on_time=row['EMIs paid on Time'],
                    approved_date=row['Date of Approval'],
                    end_date=row['End Date'],
                )
        except Customer.DoesNotExist:
            print(f"Customer with ID {row['Customer ID']} not found. Skipping this loan.")

    print("Loan data loaded successfully!")
