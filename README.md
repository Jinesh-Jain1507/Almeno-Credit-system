# **Almeno Credit System**

## **Overview**
Almeno Credit System is a backend application for managing customer credit approvals, loan processing, and eligibility checks. It is built with Django, Django REST Framework, and utilizes SQLite for data storage, ensuring ease of use and efficient development.

This system automates the handling of credit operations and loan management based on predefined business rules, leveraging data from historical transactions and customer profiles.

---

## **Features**
- **Customer Registration**:
  - Automatically calculates credit limits based on income.
  - Stores customer details such as name, age, income, and phone number.

- **Loan Eligibility Checks**:
  - Determines loan approval or rejection based on customer credit scores.
  - Credit score calculation incorporates:
    - Timeliness of past EMI payments.
    - Number of past loans.
    - Activity in the current year.
    - Approved volume of loans.
    - Current debt exceeding the approved limit.

- **Loan Management**:
  - Processes new loans with interest rates adjusted based on credit scores.
  - Calculates monthly installments using the compound interest formula.
  - Tracks repayment details and EMIs left.

- **Data Retrieval**:
  - Fetches details of a specific loan.
  - Lists all loans for a customer.

- **Dynamic Calculations**:
  - Automatically sets loan end dates based on tenure.

---

## **Technologies Used**
- **Backend Framework**: Django 4+ with Django REST Framework (DRF)
- **Database**: SQLite
- **Task Automation**: Background workers for data ingestion
- **Data Processing**: Pandas for handling customer and loan data from Excel files

---

## **Setup and Installation**

### **Prerequisites**
- Python 3.11 or later
- Git

### **Steps to Set Up**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Jinesh-Jain1507/Almeno-Credit-system.git
   cd Almeno-Credit-system
   
2. **Install Dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   pip install -r requirements.txt

1. **Run Migrations**:
   ```bash
   python manage.py migrate

1. **Start the Development Server**:
   ```bash
   python manage.py runserver

1. **Access the Application**:
   ```bash
   http://127.0.0.1:8000
