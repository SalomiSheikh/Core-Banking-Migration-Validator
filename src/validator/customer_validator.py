import csv

source_file = "data/source/customer.csv"
target_file = "data/target/customer.csv"

print("Migration Validator Started")

with open(source_file, "r") as file:
    source_data = list(csv.DictReader(file))

with open(target_file, "r") as file:
    target_data = list(csv.DictReader(file))

print("Source customers:", len(source_data))
print("Target customers:", len(target_data))

missing_count = 0
unexpected_count = 0
mismatch_count = 0

print("\nChecking customer migration...")

for source_customer in source_data:
    customer_id = source_customer["customer_id"]

    matching_customer = None

    for target_customer in target_data:
        if target_customer["customer_id"] == customer_id:
            matching_customer = target_customer
            break

    if matching_customer is None:
        print("MISSING IN TARGET:", customer_id)
        missing_count += 1

    else:
        if source_customer["name"] != matching_customer["name"]:
            print("NAME MISMATCH:", customer_id)
            print("  Source :", source_customer["name"])
            print("  Target :", matching_customer["name"])
            mismatch_count += 1

        if source_customer["status"] != matching_customer["status"]:
            print("STATUS MISMATCH:", customer_id)
            print("  Source :", source_customer["status"])
            print("  Target :", matching_customer["status"])
            mismatch_count += 1

        if source_customer["country"] != matching_customer["country"]:
            print("COUNTRY MISMATCH:", customer_id)
            print("  Source :", source_customer["country"])
            print("  Target :", matching_customer["country"])
            mismatch_count += 1


print("\nChecking for unexpected customers...")

source_ids = [customer["customer_id"] for customer in source_data]

for target_customer in target_data:
    customer_id = target_customer["customer_id"]

    if customer_id not in source_ids:
        print("UNEXPECTED IN TARGET:", customer_id)
        unexpected_count += 1


print("\n================================")
print("     MIGRATION VALIDATION REPORT")
print("================================")

print("Total Source Customers :", len(source_data))
print("Total Target Customers :", len(target_data))

print("Missing Customers      :", missing_count)
print("Unexpected Customers   :", unexpected_count)
print("Data Mismatches        :", mismatch_count)

if missing_count == 0 and unexpected_count == 0 and mismatch_count == 0:
    print("Migration Status       : PASSED")
else:
    print("Migration Status       : FAILED")

print("================================")