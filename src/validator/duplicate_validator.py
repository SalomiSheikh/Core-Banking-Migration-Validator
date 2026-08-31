import csv

files = {
    "Customer": "data/target/customer.csv",
    "Account": "data/target/account.csv",
    "Transaction": "data/target/transaction.csv"
}

print("Duplicate Record Validator Started")

total_duplicates = 0

for entity, file_path in files.items():

    print("\nChecking:", entity)

    with open(file_path, "r") as file:
        data = list(csv.DictReader(file))

    # Determine the ID column
    if entity == "Customer":
        id_column = "customer_id"
    elif entity == "Account":
        id_column = "account_id"
    else:
        id_column = "transaction_id"

    ids = [record[id_column] for record in data]

    duplicate_ids = []

    for record_id in ids:

        if ids.count(record_id) > 1 and record_id not in duplicate_ids:
            duplicate_ids.append(record_id)

    if len(duplicate_ids) == 0:

        print("No duplicates found")

    else:

        for duplicate_id in duplicate_ids:

            count = ids.count(duplicate_id)

            print("DUPLICATE RECORD:", duplicate_id)
            print("  Entity      :", entity)
            print("  Occurrences :", count)

            total_duplicates += 1


print("\n================================")
print("   DUPLICATE VALIDATION REPORT")
print("================================")

print("Duplicate Records :", total_duplicates)

if total_duplicates == 0:
    print("Duplicate Status  : PASSED")
else:
    print("Duplicate Status  : FAILED")

print("================================")