import csv


SOURCE_FILE = "data/source/transaction.csv"
TARGET_FILE = "data/target/transaction.csv"
REPORT_FILE = "reports/transaction_exception_report.txt"


def load_transactions(file_path):
    transactions = {}

    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            transactions[row["transaction_id"]] = row

    return transactions


def generate_report():

    source_transactions = load_transactions(SOURCE_FILE)
    target_transactions = load_transactions(TARGET_FILE)

    missing_transactions = []
    unexpected_transactions = []
    mismatches = []

    # Check missing transactions and field mismatches
    for transaction_id, source_record in source_transactions.items():

        if transaction_id not in target_transactions:
            missing_transactions.append(transaction_id)
            continue

        target_record = target_transactions[transaction_id]

        for field in source_record:

            if field == "transaction_id":
                continue

            if source_record[field] != target_record[field]:

                mismatches.append({
                    "transaction_id": transaction_id,
                    "field": field,
                    "source": source_record[field],
                    "target": target_record[field]
                })

    # Check unexpected transactions
    for transaction_id in target_transactions:

        if transaction_id not in source_transactions:
            unexpected_transactions.append(transaction_id)

    # Generate report
    with open(REPORT_FILE, "w", encoding="utf-8") as report:

        report.write("=" * 60 + "\n")
        report.write("          TRANSACTION MIGRATION EXCEPTION REPORT\n")
        report.write("=" * 60 + "\n\n")

        report.write("MISSING TRANSACTIONS\n")
        report.write("-" * 60 + "\n")

        if missing_transactions:
            for transaction_id in missing_transactions:
                report.write(transaction_id + "\n")
        else:
            report.write("None\n")

        report.write("\n")

        report.write("UNEXPECTED TRANSACTIONS\n")
        report.write("-" * 60 + "\n")

        if unexpected_transactions:
            for transaction_id in unexpected_transactions:
                report.write(transaction_id + "\n")
        else:
            report.write("None\n")

        report.write("\n")

        report.write("TRANSACTION FIELD MISMATCHES\n")
        report.write("-" * 60 + "\n")

        if mismatches:

            for mismatch in mismatches:

                report.write(
                    f"Transaction ID : {mismatch['transaction_id']}\n"
                )

                report.write(
                    f"Field          : {mismatch['field']}\n"
                )

                report.write(
                    f"Source         : {mismatch['source']}\n"
                )

                report.write(
                    f"Target         : {mismatch['target']}\n"
                )

                report.write("-" * 60 + "\n")

        else:
            report.write("None\n")

    print("Transaction exception report generated successfully.")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    generate_report()