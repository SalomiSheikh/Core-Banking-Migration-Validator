import csv
import os
from collections import Counter


INPUT_FILE = "reconciliation/migration_exceptions.csv"


def load_exceptions():

    with open(
        INPUT_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)


def generate_dashboard():

    if not os.path.exists(INPUT_FILE):

        print(
            f"ERROR: File not found: {INPUT_FILE}"
        )

        return

    exceptions = load_exceptions()

    total = len(exceptions)

    open_count = sum(
        1
        for row in exceptions
        if row["Status"] == "OPEN"
    )

    resolved_count = sum(
        1
        for row in exceptions
        if row["Status"] == "RESOLVED"
    )

    severity_counts = Counter(
        row["Severity"]
        for row in exceptions
    )

    entity_counts = Counter(
        row["Entity"]
        for row in exceptions
    )

    type_counts = Counter(
        row["Exception_Type"]
        for row in exceptions
    )

    print()
    print("=" * 70)
    print("             MIGRATION QUALITY DASHBOARD")
    print("=" * 70)

    print()
    print("OVERALL EXCEPTION SUMMARY")
    print("-" * 70)

    print(
        f"{'Total Exceptions':<35}: {total}"
    )

    print(
        f"{'Open Exceptions':<35}: {open_count}"
    )

    print(
        f"{'Resolved Exceptions':<35}: {resolved_count}"
    )

    print()
    print("SEVERITY SUMMARY")
    print("-" * 70)

    print(
        f"{'CRITICAL':<35}: "
        f"{severity_counts.get('CRITICAL', 0)}"
    )

    print(
        f"{'HIGH':<35}: "
        f"{severity_counts.get('HIGH', 0)}"
    )

    print()
    print("ENTITY SUMMARY")
    print("-" * 70)

    print(
        f"{'Customer':<35}: "
        f"{entity_counts.get('Customer', 0)}"
    )

    print(
        f"{'Account':<35}: "
        f"{entity_counts.get('Account', 0)}"
    )

    print(
        f"{'Transaction':<35}: "
        f"{entity_counts.get('Transaction', 0)}"
    )

    print()
    print("EXCEPTION TYPE SUMMARY")
    print("-" * 70)

    print(
        f"{'FIELD MISMATCH':<35}: "
        f"{type_counts.get('FIELD_MISMATCH', 0)}"
    )

    print(
        f"{'MISSING':<35}: "
        f"{type_counts.get('MISSING', 0)}"
    )

    print(
        f"{'UNEXPECTED':<35}: "
        f"{type_counts.get('UNEXPECTED', 0)}"
    )

    print()
    print("-" * 70)

    if open_count == 0:

        overall_status = "PASSED"

    else:

        overall_status = "FAILED"

    print(
        f"{'MIGRATION QUALITY STATUS':<35}: "
        f"{overall_status}"
    )

    print("=" * 70)


if __name__ == "__main__":
    generate_dashboard()