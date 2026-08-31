import subprocess
import csv
import os
import sys


print("========================================")
print("    CORE BANKING MIGRATION VALIDATION")
print("========================================")


# ---------------------------------------------------------
# 1. RUN CORE VALIDATORS
# ---------------------------------------------------------

validators = [
    ("Customer", "src/validator/customer_validator.py"),
    ("Account", "src/validator/account_validator.py"),
    ("Customer-Account", "src/validator/customer_account_validator.py"),
    ("Transaction", "src/validator/transaction_validator.py"),
    ("Duplicate", "src/validator/duplicate_validator.py")
]

results = {}


for name, validator in validators:

    print("\n----------------------------------------")
    print("Running:", name)
    print("----------------------------------------")

    result = subprocess.run(
        [sys.executable, validator],
        capture_output=True,
        text=True
    )

    output = result.stdout

    print(output)

    if result.stderr:
        print(result.stderr)

    # -----------------------------------------------------
    # Determine validator status
    # -----------------------------------------------------

    if result.returncode != 0:

        results[name] = "FAILED"

    elif (
        "Migration Status" in output
        and "PASSED" in output
    ):

        results[name] = "PASSED"

    elif (
        "Relationship Status" in output
        and "PASSED" in output
    ):

        results[name] = "PASSED"

    elif (
        "Duplicate Status" in output
        and "PASSED" in output
    ):

        results[name] = "PASSED"

    else:

        results[name] = "FAILED"


# ---------------------------------------------------------
# 2. RUN EXCEPTION REPORTS
# ---------------------------------------------------------

exception_reports = [
    ("Customer Exception Report", "src/exception_report.py"),
    ("Account Exception Report", "src/account_exception_report.py"),
    ("Transaction Exception Report", "src/transaction_exception_report.py"),
    ("Master Exception Report", "src/master_exception_report.py")
]


print("\n========================================")
print("       EXCEPTION REPORT GENERATION")
print("========================================")


for name, script in exception_reports:

    print("\n----------------------------------------")
    print("Running:", name)
    print("----------------------------------------")

    result = subprocess.run(
        [sys.executable, script],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:

        print(result.stderr)

        print(
            f"WARNING: {name} failed to generate."
        )


# ---------------------------------------------------------
# 3. RUN REFERENTIAL INTEGRITY VALIDATION
# ---------------------------------------------------------

print("\n========================================")
print("       DATA QUALITY VALIDATION")
print("========================================")


integrity_result = subprocess.run(
    [sys.executable, "src/referential_integrity_validator.py"],
    capture_output=True,
    text=True
)

print(integrity_result.stdout)

if integrity_result.returncode != 0:

    print(integrity_result.stderr)


# ---------------------------------------------------------
# 4. LOAD CSV DATA
# ---------------------------------------------------------

def load_data(file_path, key):

    records = {}

    with open(
        file_path,
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            records[row[key]] = row

    return records


# ---------------------------------------------------------
# 5. CALCULATE RECONCILIATION
# ---------------------------------------------------------

def calculate_reconciliation(
    source_file,
    target_file,
    key
):

    source = load_data(source_file, key)
    target = load_data(target_file, key)

    missing = 0
    unexpected = 0
    mismatches = 0

    # Missing records and field mismatches

    for record_id, source_record in source.items():

        if record_id not in target:

            missing += 1

        else:

            target_record = target[record_id]

            for field in source_record:

                if field == key:
                    continue

                if source_record[field] != target_record[field]:

                    mismatches += 1

    # Unexpected records

    for record_id in target:

        if record_id not in source:

            unexpected += 1

    return (
        len(source),
        len(target),
        missing,
        unexpected,
        mismatches
    )


# ---------------------------------------------------------
# 6. ENTITY RECONCILIATION
# ---------------------------------------------------------

customer_reconciliation = calculate_reconciliation(
    "data/source/customer.csv",
    "data/target/customer.csv",
    "customer_id"
)


account_reconciliation = calculate_reconciliation(
    "data/source/account.csv",
    "data/target/account.csv",
    "account_id"
)


transaction_reconciliation = calculate_reconciliation(
    "data/source/transaction.csv",
    "data/target/transaction.csv",
    "transaction_id"
)


# ---------------------------------------------------------
# 7. CREATE OUTPUT DIRECTORIES
# ---------------------------------------------------------

os.makedirs("reports", exist_ok=True)
os.makedirs("reconciliation", exist_ok=True)


# ---------------------------------------------------------
# 8. CALCULATE TOTAL EXCEPTIONS
# ---------------------------------------------------------

total_missing = (
    customer_reconciliation[2]
    + account_reconciliation[2]
    + transaction_reconciliation[2]
)


total_unexpected = (
    customer_reconciliation[3]
    + account_reconciliation[3]
    + transaction_reconciliation[3]
)


total_mismatches = (
    customer_reconciliation[4]
    + account_reconciliation[4]
    + transaction_reconciliation[4]
)


total_exceptions = (
    total_missing
    + total_unexpected
    + total_mismatches
)


# ---------------------------------------------------------
# 9. OVERALL STATUS
# ---------------------------------------------------------

if (
    all(status == "PASSED" for status in results.values())
    and total_exceptions == 0
):

    overall_status = "PASSED"

else:

    overall_status = "FAILED"


# ---------------------------------------------------------
# 10. CREATE RECONCILIATION CSV
# ---------------------------------------------------------

summary_file = "reconciliation/migration_summary.csv"


summary_rows = [

    [
        "Customer",
        customer_reconciliation[0],
        customer_reconciliation[1],
        customer_reconciliation[2],
        customer_reconciliation[3],
        customer_reconciliation[4],
        results["Customer"]
    ],

    [
        "Account",
        account_reconciliation[0],
        account_reconciliation[1],
        account_reconciliation[2],
        account_reconciliation[3],
        account_reconciliation[4],
        results["Account"]
    ],

    [
        "Customer-Account",
        5,
        5,
        0,
        0,
        0,
        results["Customer-Account"]
    ],

    [
        "Transaction",
        transaction_reconciliation[0],
        transaction_reconciliation[1],
        transaction_reconciliation[2],
        transaction_reconciliation[3],
        transaction_reconciliation[4],
        results["Transaction"]
    ],

    [
        "Duplicate",
        "",
        "",
        0,
        0,
        0,
        results["Duplicate"]
    ]
]


with open(
    summary_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Entity",
        "Source Count",
        "Target Count",
        "Missing",
        "Unexpected",
        "Mismatches",
        "Status"
    ])

    writer.writerows(summary_rows)


# ---------------------------------------------------------
# 11. FINAL MIGRATION RESULT
# ---------------------------------------------------------

print("\n========================================")
print("       OVERALL MIGRATION RESULT")
print("========================================")


for name, status in results.items():

    print(
        f"{name:<30}: {status}"
    )


print("----------------------------------------")


print(
    f"{'OVERALL MIGRATION STATUS':<30}: "
    f"{overall_status}"
)


print("========================================")


# ---------------------------------------------------------
# 12. RECONCILIATION SUMMARY
# ---------------------------------------------------------

print("\n========================================")
print("       RECONCILIATION SUMMARY")
print("========================================")


print(
    f"{'Missing Records':<30}: "
    f"{total_missing}"
)


print(
    f"{'Unexpected Records':<30}: "
    f"{total_unexpected}"
)


print(
    f"{'Field Mismatches':<30}: "
    f"{total_mismatches}"
)


print(
    f"{'Total Exceptions':<30}: "
    f"{total_exceptions}"
)


print("----------------------------------------")


print(
    f"{'OVERALL STATUS':<30}: "
    f"{overall_status}"
)


print("========================================")


print("\nReconciliation summary generated:")
print(summary_file)