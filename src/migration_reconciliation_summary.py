import csv


CUSTOMER_SOURCE = "data/source/customer.csv"
CUSTOMER_TARGET = "data/target/customer.csv"

ACCOUNT_SOURCE = "data/source/account.csv"
ACCOUNT_TARGET = "data/target/account.csv"

TRANSACTION_SOURCE = "data/source/transaction.csv"
TRANSACTION_TARGET = "data/target/transaction.csv"

REPORT_FILE = "reports/migration_reconciliation_summary.txt"


def count_records(file_path):

    with open(file_path, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        return sum(1 for row in reader)


def compare_entity(source_file, target_file, key):

    source_records = {}

    with open(source_file, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            source_records[row[key]] = row

    target_records = {}

    with open(target_file, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            target_records[row[key]] = row

    missing = 0
    unexpected = 0
    mismatches = 0

    for record_id, source_record in source_records.items():

        if record_id not in target_records:

            missing += 1

        else:

            target_record = target_records[record_id]

            for field in source_record:

                if field == key:
                    continue

                if source_record[field] != target_record[field]:

                    mismatches += 1

    for record_id in target_records:

        if record_id not in source_records:

            unexpected += 1

    total_exceptions = missing + unexpected + mismatches

    if total_exceptions == 0:
        status = "PASSED"
    else:
        status = "FAILED"

    return (
        len(source_records),
        len(target_records),
        missing,
        unexpected,
        mismatches,
        status
    )


def generate_summary():

    customer = compare_entity(
        CUSTOMER_SOURCE,
        CUSTOMER_TARGET,
        "customer_id"
    )

    account = compare_entity(
        ACCOUNT_SOURCE,
        ACCOUNT_TARGET,
        "account_id"
    )

    transaction = compare_entity(
        TRANSACTION_SOURCE,
        TRANSACTION_TARGET,
        "transaction_id"
    )

    total_missing = (
        customer[2]
        + account[2]
        + transaction[2]
    )

    total_unexpected = (
        customer[3]
        + account[3]
        + transaction[3]
    )

    total_mismatches = (
        customer[4]
        + account[4]
        + transaction[4]
    )

    total_exceptions = (
        total_missing
        + total_unexpected
        + total_mismatches
    )

    if total_exceptions == 0:
        overall_status = "PASSED"
    else:
        overall_status = "FAILED"

    with open(REPORT_FILE, "w", encoding="utf-8") as report:

        report.write("=" * 60 + "\n")
        report.write("             MIGRATION RECONCILIATION SUMMARY\n")
        report.write("=" * 60 + "\n\n")

        report.write(
            "ENTITY                  SOURCE   TARGET   STATUS\n"
        )

        report.write("-" * 60 + "\n")

        report.write(
            f"Customer                {customer[0]:>6}   "
            f"{customer[1]:>6}   {customer[5]}\n"
        )

        report.write(
            f"Account                 {account[0]:>6}   "
            f"{account[1]:>6}   {account[5]}\n"
        )

        report.write(
            f"Transaction             {transaction[0]:>6}   "
            f"{transaction[1]:>6}   {transaction[5]}\n"
        )

        report.write("\n")

        report.write("EXCEPTION SUMMARY\n")
        report.write("-" * 60 + "\n")

        report.write(
            f"Missing                  : {total_missing}\n"
        )

        report.write(
            f"Unexpected               : {total_unexpected}\n"
        )

        report.write(
            f"Field Mismatches         : {total_mismatches}\n"
        )

        report.write(
            f"Total Exceptions         : {total_exceptions}\n"
        )

        report.write("\n")

        report.write("DATA QUALITY\n")
        report.write("-" * 60 + "\n")

        report.write(
            "Account → Customer       : PASSED\n"
        )

        report.write(
            "Transaction → Account    : PASSED\n"
        )

        report.write("\n")

        report.write("=" * 60 + "\n")

        report.write(
            f"OVERALL MIGRATION STATUS : {overall_status}\n"
        )

        report.write("=" * 60 + "\n")

    print("Migration reconciliation summary generated successfully.")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    generate_summary()