import csv


SOURCE_FILE = "data/source/account.csv"
TARGET_FILE = "data/target/account.csv"
REPORT_FILE = "reports/account_exception_report.txt"


def load_accounts(file_path):
    accounts = {}

    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            accounts[row["account_id"]] = row

    return accounts


def generate_report():

    source_accounts = load_accounts(SOURCE_FILE)
    target_accounts = load_accounts(TARGET_FILE)

    missing_accounts = []
    unexpected_accounts = []
    mismatches = []

    # Check for missing accounts and field mismatches
    for account_id, source_record in source_accounts.items():

        if account_id not in target_accounts:
            missing_accounts.append(account_id)
            continue

        target_record = target_accounts[account_id]

        for field in source_record:

            if field == "account_id":
                continue

            if source_record[field] != target_record[field]:

                mismatches.append({
                    "account_id": account_id,
                    "field": field,
                    "source": source_record[field],
                    "target": target_record[field]
                })

    # Check for unexpected accounts
    for account_id in target_accounts:

        if account_id not in source_accounts:
            unexpected_accounts.append(account_id)

    # Create report
    with open(REPORT_FILE, "w", encoding="utf-8") as report:

        report.write("=" * 60 + "\n")
        report.write("             ACCOUNT MIGRATION EXCEPTION REPORT\n")
        report.write("=" * 60 + "\n\n")

        report.write("MISSING ACCOUNTS\n")
        report.write("-" * 60 + "\n")

        if missing_accounts:
            for account_id in missing_accounts:
                report.write(account_id + "\n")
        else:
            report.write("None\n")

        report.write("\n")

        report.write("UNEXPECTED ACCOUNTS\n")
        report.write("-" * 60 + "\n")

        if unexpected_accounts:
            for account_id in unexpected_accounts:
                report.write(account_id + "\n")
        else:
            report.write("None\n")

        report.write("\n")

        report.write("ACCOUNT FIELD MISMATCHES\n")
        report.write("-" * 60 + "\n")

        if mismatches:

            for mismatch in mismatches:

                report.write(
                    f"Account ID  : {mismatch['account_id']}\n"
                )

                report.write(
                    f"Field       : {mismatch['field']}\n"
                )

                report.write(
                    f"Source      : {mismatch['source']}\n"
                )

                report.write(
                    f"Target      : {mismatch['target']}\n"
                )

                report.write("-" * 60 + "\n")

        else:
            report.write("None\n")

    print("Account exception report generated successfully.")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    generate_report()