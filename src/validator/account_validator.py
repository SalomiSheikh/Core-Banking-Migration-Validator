import csv

source_file = "data/source/account.csv"
target_file = "data/target/account.csv"

print("Account Migration Validator Started")

with open(source_file, "r") as file:
    source_data = list(csv.DictReader(file))

with open(target_file, "r") as file:
    target_data = list(csv.DictReader(file))

print("Source accounts:", len(source_data))
print("Target accounts:", len(target_data))

missing_count = 0
unexpected_count = 0
mismatch_count = 0

print("\nChecking account migration...")

for source_account in source_data:

    account_id = source_account["account_id"]

    matching_account = None

    for target_account in target_data:
        if target_account["account_id"] == account_id:
            matching_account = target_account
            break

    if matching_account is None:
        print("MISSING IN TARGET:", account_id)
        missing_count += 1

    else:

        if source_account["customer_id"] != matching_account["customer_id"]:
            print("CUSTOMER ID MISMATCH:", account_id)
            print("  Source :", source_account["customer_id"])
            print("  Target :", matching_account["customer_id"])
            mismatch_count += 1

        if source_account["account_type"] != matching_account["account_type"]:
            print("ACCOUNT TYPE MISMATCH:", account_id)
            print("  Source :", source_account["account_type"])
            print("  Target :", matching_account["account_type"])
            mismatch_count += 1

        if source_account["currency"] != matching_account["currency"]:
            print("CURRENCY MISMATCH:", account_id)
            print("  Source :", source_account["currency"])
            print("  Target :", matching_account["currency"])
            mismatch_count += 1

        if source_account["balance"] != matching_account["balance"]:
            print("BALANCE MISMATCH:", account_id)
            print("  Source :", source_account["balance"])
            print("  Target :", matching_account["balance"])
            mismatch_count += 1

        if source_account["status"] != matching_account["status"]:
            print("STATUS MISMATCH:", account_id)
            print("  Source :", source_account["status"])
            print("  Target :", matching_account["status"])
            mismatch_count += 1


print("\nChecking for unexpected accounts...")

source_ids = [account["account_id"] for account in source_data]

for target_account in target_data:

    account_id = target_account["account_id"]

    if account_id not in source_ids:
        print("UNEXPECTED IN TARGET:", account_id)
        unexpected_count += 1


print("\n================================")
print("     ACCOUNT MIGRATION REPORT")
print("================================")

print("Total Source Accounts :", len(source_data))
print("Total Target Accounts :", len(target_data))

print("Missing Accounts      :", missing_count)
print("Unexpected Accounts   :", unexpected_count)
print("Data Mismatches       :", mismatch_count)

if missing_count == 0 and unexpected_count == 0 and mismatch_count == 0:
    print("Migration Status      : PASSED")
else:
    print("Migration Status      : FAILED")

print("================================")