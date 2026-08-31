import csv


SOURCE_CUSTOMER = "data/source/customer.csv"
TARGET_CUSTOMER = "data/target/customer.csv"

SOURCE_ACCOUNT = "data/source/account.csv"
TARGET_ACCOUNT = "data/target/account.csv"

SOURCE_TRANSACTION = "data/source/transaction.csv"
TARGET_TRANSACTION = "data/target/transaction.csv"

REPORT_FILE = "reports/master_migration_exception_report.txt"


def load_data(file_path, key):

    records = {}

    with open(file_path, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            records[row[key]] = row

    return records


def compare_data(source_file, target_file, key):

    source_data = load_data(source_file, key)
    target_data = load_data(target_file, key)

    missing = []
    unexpected = []
    mismatches = []

    # Check source records
    for record_id, source_record in source_data.items():

        if record_id not in target_data:

            missing.append(record_id)

        else:

            target_record = target_data[record_id]

            for field in source_record:

                if field == key:
                    continue

                if source_record[field] != target_record[field]:

                    mismatches.append({
                        "id": record_id,
                        "field": field,
                        "source": source_record[field],
                        "target": target_record[field]
                    })

    # Check target records
    for record_id in target_data:

        if record_id not in source_data:

            unexpected.append(record_id)

    return missing, unexpected, mismatches


def write_section(report, entity_name, missing, unexpected, mismatches):

    report.write(f"{entity_name.upper()} EXCEPTIONS\n")
    report.write("-" * 60 + "\n")

    report.write(f"Missing       : {len(missing)}\n")
    report.write(f"Unexpected    : {len(unexpected)}\n")
    report.write(f"Mismatches    : {len(mismatches)}\n")
    report.write(
        f"Total         : {len(missing) + len(unexpected) + len(mismatches)}\n"
    )

    report.write("\n")


def generate_report():

    customer_missing, customer_unexpected, customer_mismatches = compare_data(
        SOURCE_CUSTOMER,
        TARGET_CUSTOMER,
        "customer_id"
    )

    account_missing, account_unexpected, account_mismatches = compare_data(
        SOURCE_ACCOUNT,
        TARGET_ACCOUNT,
        "account_id"
    )

    transaction_missing, transaction_unexpected, transaction_mismatches = compare_data(
        SOURCE_TRANSACTION,
        TARGET_TRANSACTION,
        "transaction_id"
    )

    total_missing = (
        len(customer_missing)
        + len(account_missing)
        + len(transaction_missing)
    )

    total_unexpected = (
        len(customer_unexpected)
        + len(account_unexpected)
        + len(transaction_unexpected)
    )

    total_mismatches = (
        len(customer_mismatches)
        + len(account_mismatches)
        + len(transaction_mismatches)
    )

    total_exceptions = (
        total_missing
        + total_unexpected
        + total_mismatches
    )

    with open(REPORT_FILE, "w", encoding="utf-8") as report:

        report.write("=" * 60 + "\n")
        report.write("          MASTER MIGRATION EXCEPTION REPORT\n")
        report.write("=" * 60 + "\n\n")

        write_section(
            report,
            "Customer",
            customer_missing,
            customer_unexpected,
            customer_mismatches
        )

        write_section(
            report,
            "Account",
            account_missing,
            account_unexpected,
            account_mismatches
        )

        write_section(
            report,
            "Transaction",
            transaction_missing,
            transaction_unexpected,
            transaction_mismatches
        )

        report.write("=" * 60 + "\n")
        report.write("OVERALL EXCEPTION SUMMARY\n")
        report.write("=" * 60 + "\n")

        report.write(f"Total Missing       : {total_missing}\n")
        report.write(f"Total Unexpected    : {total_unexpected}\n")
        report.write(f"Total Mismatches    : {total_mismatches}\n")
        report.write(f"TOTAL EXCEPTIONS    : {total_exceptions}\n")

        if total_exceptions == 0:
            report.write("OVERALL STATUS      : PASSED\n")
        else:
            report.write("OVERALL STATUS      : FAILED\n")

    print("Master migration exception report generated successfully.")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    generate_report()