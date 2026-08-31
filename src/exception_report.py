import csv
import os


SOURCE_FILE = "data/source/customer.csv"
TARGET_FILE = "data/target/customer.csv"
REPORT_FILE = "reports/customer_exception_report.txt"


def read_csv(file_path):
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def generate_customer_exception_report():

    if not os.path.exists(SOURCE_FILE):
        print(f"ERROR: Source file not found: {SOURCE_FILE}")
        return

    if not os.path.exists(TARGET_FILE):
        print(f"ERROR: Target file not found: {TARGET_FILE}")
        return

    source_records = read_csv(SOURCE_FILE)
    target_records = read_csv(TARGET_FILE)

    source_data = {
        row["customer_id"]: row
        for row in source_records
    }

    target_data = {
        row["customer_id"]: row
        for row in target_records
    }

    source_ids = set(source_data.keys())
    target_ids = set(target_data.keys())

    missing_ids = source_ids - target_ids
    unexpected_ids = target_ids - source_ids

    common_ids = source_ids & target_ids

    mismatches = []

    for customer_id in common_ids:

        source_record = source_data[customer_id]
        target_record = target_data[customer_id]

        for field in source_record:

            if field == "customer_id":
                continue

            if source_record[field] != target_record[field]:

                mismatches.append({
                    "customer_id": customer_id,
                    "field": field,
                    "source_value": source_record[field],
                    "target_value": target_record[field]
                })

    os.makedirs("reports", exist_ok=True)

    with open(REPORT_FILE, mode="w", encoding="utf-8") as report:

        report.write("=" * 60 + "\n")
        report.write("          CUSTOMER MIGRATION EXCEPTION REPORT\n")
        report.write("=" * 60 + "\n\n")

        report.write("MISSING CUSTOMERS\n")
        report.write("-" * 60 + "\n")

        if missing_ids:
            for customer_id in sorted(missing_ids):
                report.write(f"{customer_id}\n")
        else:
            report.write("None\n")

        report.write("\nUNEXPECTED CUSTOMERS\n")
        report.write("-" * 60 + "\n")

        if unexpected_ids:
            for customer_id in sorted(unexpected_ids):
                report.write(f"{customer_id}\n")
        else:
            report.write("None\n")

        report.write("\nCUSTOMER FIELD MISMATCHES\n")
        report.write("-" * 60 + "\n")

        if mismatches:

            for mismatch in mismatches:

                report.write(
                    f"Customer ID : {mismatch['customer_id']}\n"
                )

                report.write(
                    f"Field       : {mismatch['field']}\n"
                )

                report.write(
                    f"Source      : {mismatch['source_value']}\n"
                )

                report.write(
                    f"Target      : {mismatch['target_value']}\n"
                )

                report.write("-" * 60 + "\n")

        else:
            report.write("None\n")

    print("Customer exception report generated:")
    print(REPORT_FILE)


if __name__ == "__main__":
    generate_customer_exception_report()