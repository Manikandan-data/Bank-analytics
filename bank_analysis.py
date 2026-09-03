import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="bank_analytics"
)

customers_df = pd.read_sql("SELECT * FROM customers", conn)
accounts_df = pd.read_sql("SELECT * FROM accounts", conn)
transactions_df = pd.read_sql("SELECT * FROM transactions", conn)
loans_df = pd.read_sql("SELECT * FROM loans", conn)

print("Customers shape:", customers_df.shape)
print("Accounts shape:", accounts_df.shape)
print("Transactions shape:", transactions_df.shape)
print("Loans shape:", loans_df.shape)

print(customers_df.isnull().sum())
print(accounts_df.isnull().sum())
print(transactions_df.isnull().sum())
print(loans_df.isnull().sum())

print("Customers duplicates:", customers_df.duplicated().sum())
print("Accounts duplicates:", accounts_df.duplicated().sum())
print("Transactions duplicates:", transactions_df.duplicated().sum())
print("Loans duplicates:", loans_df.duplicated().sum())



customers_df["signup_date"] = pd.to_datetime(customers_df["signup_date"])

print("\nCustomers data types:")
print(customers_df.dtypes)

print("\nAccounts data types:")
print(accounts_df.dtypes)

print("\nTransactions data types:")
print(transactions_df.dtypes)

print("\nLoans data types:")
print(loans_df.dtypes)

print("Gender:", customers_df["gender"].unique())
print("Account Types:", accounts_df["account_type"].unique())
print("Transaction Types:", transactions_df["transaction_type"].unique())
print("Loan Types:", loans_df["loan_type"].unique())
print("Loan Status:", loans_df["loan_status"].unique())

print("Customer ID unique:", customers_df["customer_id"].is_unique)
print("Account ID unique:", accounts_df["account_id"].is_unique)
print("Transaction ID unique:", transactions_df["transaction_id"].is_unique)
print("Loan ID unique:", loans_df["loan_id"].is_unique)

print("Negative balance:",
      (accounts_df["balance"]<0).sum())
print("Negative transaction amounts:",
      (transactions_df["amount"] < 0).sum())

print("Negative loan amounts:",
      (loans_df["loan_amount"] < 0).sum())

print("Invalid interest rate:")
print(((loans_df["interest_rate"]<0)|
(loans_df["interest_rate"]>100)).sum())

print("Invalid signup dates:",
      pd.to_datetime(customers_df["signup_date"], errors="coerce").isnull().sum())

print("Invalid account open dates:",
      pd.to_datetime(accounts_df["open_date"], errors="coerce").isnull().sum())

print("Invalid transaction dates:",
      pd.to_datetime(transactions_df["transaction_date"], errors="coerce").isnull().sum())

customers_df["signup_date"] = pd.to_datetime(customers_df["signup_date"])

accounts_df["open_date"] = pd.to_datetime(accounts_df["open_date"])

transactions_df["transaction_date"] = pd.to_datetime(
    transactions_df["transaction_date"])

print(customers_df.dtypes)
print(accounts_df.dtypes)
print(transactions_df.dtypes)

customers_df["customer_name"] = customers_df["customer_name"].str.strip()
customers_df["gender"] = customers_df["gender"].str.strip().str.lower()
customers_df["city"] = customers_df["city"].str.strip().str.title()
customers_df["state"] = customers_df["state"].str.strip().str.title()

customers_df["signup_year"] = customers_df["signup_date"].dt.year
customers_df["signup_month"] = customers_df["signup_date"].dt.month

print(customers_df[["signup_date", "signup_year", "signup_month"]])

transactions_df["transaction_year"] = transactions_df["transaction_date"].dt.year
transactions_df["transaction_month"] = transactions_df["transaction_date"].dt.month

print(
    transactions_df[
        ["transaction_date", "transaction_year", "transaction_month"]
    ])

accounts_df["open_year"] = accounts_df["open_date"].dt.year
accounts_df["open_month"] = accounts_df["open_date"].dt.month

print(accounts_df[["open_date", "open_year", "open_month"]])

print("\nCustomers:")
print(customers_df.head())

print("\nAccounts:")
print(accounts_df.head())

print("\nTransactions:")
print(transactions_df.head())

print("\nLoans:")
print(loans_df.head())

customers_df.to_csv("customers_cleaned.csv", index=False)
accounts_df.to_csv("accounts_cleaned.csv", index=False)
transactions_df.to_csv("transactions_cleaned.csv", index=False)
loans_df.to_csv("loans_cleaned.csv", index=False)

# Customers by Gender Chart

plt.figure()
gender_count = customers_df["gender"].value_counts()

plt.bar(gender_count.index, gender_count.values)

plt.title("Customers by Gender")
plt.xlabel("Gender")
plt.ylabel("Number of Customers")
plt.tight_layout()

plt.show()

# Customers by City Chart

plt.figure()
city_count = customers_df["city"].value_counts()

plt.bar(city_count.index, city_count.values)

plt.title("Customers by City")
plt.xlabel("City")
plt.ylabel("Number of Customers")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

# Account Balance by Account Type

account_balance = accounts_df.groupby("account_type")["balance"].sum()

plt.figure()

plt.bar(account_balance.index, account_balance.values)

plt.title("Total Balance by Account Type")
plt.xlabel("Account Type")
plt.ylabel("Total Balance")
plt.tight_layout()


plt.show()

# Account Type Distribution

account_type_count = accounts_df["account_type"].value_counts()

plt.figure()

plt.bar(account_type_count.index, account_type_count.values)

plt.title("Accounts by Account Type")
plt.xlabel("Account Type")
plt.ylabel("Number of Accounts")
plt.tight_layout()


plt.show()

# Transaction Type Distribution

transaction_type_count = transactions_df["transaction_type"].value_counts()

plt.figure()

plt.bar(transaction_type_count.index, transaction_type_count.values)

plt.title("Transactions by Transaction Type")
plt.xlabel("Transaction Type")
plt.ylabel("Number of Transactions")
plt.tight_layout()


plt.show()

transaction_amount=transactions_df.groupby("transaction_type")["amount"].sum()
plt.figure()
plt.bar(transaction_amount.index,transaction_amount.values)
plt.title("Total Transaction Amount by Type")
plt.xlabel("Transaction Type")
plt.ylabel("Total Amount")
plt.tight_layout()


plt.show()

loan_amount = loans_df.groupby("loan_type")["loan_amount"].sum()

plt.figure()

plt.bar(loan_amount.index, loan_amount.values)

plt.title("Total Loan Amount by Loan Type")
plt.xlabel("Loan Type")
plt.ylabel("Total Loan Amount")
plt.tight_layout()


plt.show()

loan_status_count = loans_df["loan_status"].value_counts()

plt.figure()

plt.bar(loan_status_count.index, loan_status_count.values)

plt.title("Loans by Loan Status")
plt.xlabel("Loan Status")
plt.ylabel("Number of Loans")
plt.tight_layout()


plt.show()
monthly_transactions = transactions_df.groupby("transaction_month")["amount"].sum()

plt.figure()

plt.plot(
    monthly_transactions.index,
    monthly_transactions.values,
    marker="o"
)

plt.title("Monthly Transaction Amount")
plt.xlabel("Month")
plt.ylabel("Total Transaction Amount")
plt.tight_layout()

plt.show()

monthly_customers = customers_df["signup_month"].value_counts().sort_index()

plt.figure()

plt.bar(
    monthly_customers.index,
    monthly_customers.values
)

plt.title("Customers Signup by Month")
plt.xlabel("Month")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.show()

monthly_accounts = accounts_df["open_month"].value_counts().sort_index()

plt.figure()

plt.bar(
    monthly_accounts.index,
    monthly_accounts.values
)

plt.title("Accounts Opened by Month")
plt.xlabel("Month")
plt.ylabel("Number of Accounts")

plt.tight_layout()
plt.show()



