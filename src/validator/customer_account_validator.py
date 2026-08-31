import csv

customer_file = "data/target/customer.csv"
account_file = "data/target/account.csv"

print("Customer-Account Relationship Validator Started")

with open(customer_file, "r") as file:
    customers = list(csv.DictReader(file))

with open(account_file, "r") as file:
    accounts = list(csv.DictReader(file))

print("Target customers:", len(customers))
print("Target accounts:", len(accounts))

customer_ids = [customer["customer_id"] for customer in customers]

orphan_count = 0

print("\nChecking customer-account relationships...")

for account in accounts:

    account_id = account["account_id"]
    customer_id = account["customer_id"]

    if customer_id not in customer_ids:
        print("ORPHAN ACCOUNT:", account_id)
        print("  Customer ID:", customer_id)
        orphan_count += 1


print("\n================================")
print(" CUSTOMER-ACCOUNT VALIDATION")
print("================================")

print("Target Customers :", len(customers))
print("Target Accounts  :", len(accounts))
print("Orphan Accounts  :", orphan_count)

if orphan_count == 0:
    print("Relationship Status : PASSED")
else:
    print("Relationship Status : FAILED")

print("================================")