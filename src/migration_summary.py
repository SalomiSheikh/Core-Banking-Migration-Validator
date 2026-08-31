import csv
import os

SUMMARY_FILE = "reconciliation/migration_summary.csv"


def generate_summary():

    if not os.path.exists(SUMMARY_FILE):
        print(f"ERROR: Summary file not found: {SUMMARY_FILE}")
        return

    rows = []

    with open(SUMMARY_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append(row)

    total_entities = len(rows)

    passed = sum(
        1 for row in rows
        if row["Status"].upper() == "PASSED"
    )

    failed = sum(
        1 for row in rows
        if row["Status"].upper() == "FAILED"
    )

    total_missing = sum(
        int(row["Missing"] or 0)
        for row in rows
    )

    total_unexpected = sum(
        int(row["Unexpected"] or 0)
        for row in rows
    )

    total_mismatches = sum(
        int(row["Mismatches"] or 0)
        for row in rows
    )

    overall_status = "PASSED" if failed == 0 else "FAILED"

    print()
    print("=" * 45)
    print("       MIGRATION VALIDATION SUMMARY")
    print("=" * 45)

    print(f"Entities Validated : {total_entities}")
    print(f"Passed             : {passed}")
    print(f"Failed             : {failed}")

    print()
    print(f"Total Missing      : {total_missing}")
    print(f"Total Unexpected   : {total_unexpected}")
    print(f"Total Mismatches   : {total_mismatches}")

    print()
    print(f"Overall Status     : {overall_status}")

    print()
    print("-" * 45)
    print(f"{'Entity':<20} {'Status':<10}")
    print("-" * 45)

    for row in rows:
        print(
            f"{row['Entity']:<20} "
            f"{row['Status']:<10}"
        )

    print("-" * 45)
    print()


if __name__ == "__main__":
    generate_summary()