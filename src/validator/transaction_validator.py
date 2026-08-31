import csv

source_file = "data/source/transaction.csv"
target_file = "data/target/transaction.csv"

print("Transaction Migration Validator Started")

with open(source_file, "r") as file:
    source_data = list(csv.DictReader(file))

with open(target_file, "r") as file:
    target_data = list(csv.DictReader(file))

print("Source transactions:", len(source_data))
print("Target transactions:", len(target_data))

missing_count = 0
unexpected_count = 0
mismatch_count = 0

print("\nChecking transaction migration...")

for source_transaction in source_data:

    transaction_id = source_transaction["transaction_id"]

    matching_transaction = None

    for target_transaction in target_data:
        if target_transaction["transaction_id"] == transaction_id:
            matching_transaction = target_transaction
            break

    if matching_transaction is None:
        print("MISSING IN TARGET:", transaction_id)
        missing_count += 1

    else:

        if source_transaction["account_id"] != matching_transaction["account_id"]:
            print("ACCOUNT ID MISMATCH:", transaction_id)
            print("  Source :", source_transaction["account_id"])
            print("  Target :", matching_transaction["account_id"])
            mismatch_count += 1

        if source_transaction["transaction_type"] != matching_transaction["transaction_type"]:
            print("TRANSACTION TYPE MISMATCH:", transaction_id)
            print("  Source :", source_transaction["transaction_type"])
            print("  Target :", matching_transaction["transaction_type"])
            mismatch_count += 1

        if source_transaction["amount"] != matching_transaction["amount"]:
            print("AMOUNT MISMATCH:", transaction_id)
            print("  Source :", source_transaction["amount"])
            print("  Target :", matching_transaction["amount"])
            mismatch_count += 1

        if source_transaction["currency"] != matching_transaction["currency"]:
            print("CURRENCY MISMATCH:", transaction_id)
            print("  Source :", source_transaction["currency"])
            print("  Target :", matching_transaction["currency"])
            mismatch_count += 1

        if source_transaction["transaction_date"] != matching_transaction["transaction_date"]:
            print("DATE MISMATCH:", transaction_id)
            print("  Source :", source_transaction["transaction_date"])
            print("  Target :", matching_transaction["transaction_date"])
            mismatch_count += 1

        if source_transaction["status"] != matching_transaction["status"]:
            print("STATUS MISMATCH:", transaction_id)
            print("  Source :", source_transaction["status"])
            print("  Target :", matching_transaction["status"])
            mismatch_count += 1


print("\nChecking for unexpected transactions...")

source_ids = [transaction["transaction_id"] for transaction in source_data]

for target_transaction in target_data:

    transaction_id = target_transaction["transaction_id"]

    if transaction_id not in source_ids:
        print("UNEXPECTED IN TARGET:", transaction_id)
        unexpected_count += 1


print("\n================================")
print("  TRANSACTION MIGRATION REPORT")
print("================================")

print("Total Source Transactions :", len(source_data))
print("Total Target Transactions :", len(target_data))

print("Missing Transactions       :", missing_count)
print("Unexpected Transactions    :", unexpected_count)
print("Data Mismatches            :", mismatch_count)

if missing_count == 0 and unexpected_count == 0 and mismatch_count == 0:
    print("Migration Status           : PASSED")
else:
    print("Migration Status           : FAILED")

print("================================")