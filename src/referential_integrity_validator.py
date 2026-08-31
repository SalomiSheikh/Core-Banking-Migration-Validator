import csv


CUSTOMER_FILE = "data/target/customer.csv"
ACCOUNT_FILE = "data/target/account.csv"
TRANSACTION_FILE = "data/target/transaction.csv"

REPORT_FILE = "reports/referential_integrity_report.txt"


def load_column(file_path, column_name):

    values = set()

    with open(file_path, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            values.add(row[column_name])

    return values


def check_account_customer_relationship():

    customer_ids = load_column(
        CUSTOMER_FILE,
        "customer_id"
    )

    orphan_accounts = []

    with open(ACCOUNT_FILE, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            customer_id = row["customer_id"]

            if customer_id not in customer_ids:

                orphan_accounts.append({
                    "account_id": row["account_id"],
                    "customer_id": customer_id
                })

    return orphan_accounts


def check_transaction_account_relationship():

    account_ids = load_column(
        ACCOUNT_FILE,
        "account_id"
    )

    orphan_transactions = []

    with open(TRANSACTION_FILE, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            account_id = row["account_id"]

            if account_id not in account_ids:

                orphan_transactions.append({
                    "transaction_id": row["transaction_id"],
                    "account_id": account_id
                })

    return orphan_transactions


def generate_report():

    orphan_accounts = check_account_customer_relationship()

    orphan_transactions = check_transaction_account_relationship()

    total_exceptions = (
        len(orphan_accounts)
        + len(orphan_transactions)
    )

    with open(REPORT_FILE, "w", encoding="utf-8") as report:

        report.write("=" * 60 + "\n")
        report.write("       REFERENTIAL INTEGRITY VALIDATION REPORT\n")
        report.write("=" * 60 + "\n\n")

        # Account → Customer
        report.write("ACCOUNT → CUSTOMER VALIDATION\n")
        report.write("-" * 60 + "\n")

        if orphan_accounts:

            report.write("ORPHAN ACCOUNTS FOUND\n\n")

            for record in orphan_accounts:

                report.write(
                    f"Account ID  : {record['account_id']}\n"
                )

                report.write(
                    f"Customer ID : {record['customer_id']}\n"
                )

                report.write("-" * 60 + "\n")

        else:

            report.write("PASSED - All accounts have valid customers.\n")

        report.write("\n")

        # Transaction → Account
        report.write("TRANSACTION → ACCOUNT VALIDATION\n")
        report.write("-" * 60 + "\n")

        if orphan_transactions:

            report.write("ORPHAN TRANSACTIONS FOUND\n\n")

            for record in orphan_transactions:

                report.write(
                    f"Transaction ID : {record['transaction_id']}\n"
                )

                report.write(
                    f"Account ID     : {record['account_id']}\n"
                )

                report.write("-" * 60 + "\n")

        else:

            report.write("PASSED - All transactions have valid accounts.\n")

        report.write("\n")

        # Overall status
        report.write("=" * 60 + "\n")
        report.write("OVERALL DATA QUALITY STATUS\n")
        report.write("=" * 60 + "\n")

        report.write(
            f"Orphan Accounts     : {len(orphan_accounts)}\n"
        )

        report.write(
            f"Orphan Transactions  : {len(orphan_transactions)}\n"
        )

        report.write(
            f"Total Exceptions     : {total_exceptions}\n"
        )

        if total_exceptions == 0:

            report.write("STATUS              : PASSED\n")

        else:

            report.write("STATUS              : FAILED\n")

    print("Referential integrity report generated successfully.")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    generate_report()