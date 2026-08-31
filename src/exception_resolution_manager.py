import csv
import os


INPUT_FILE = "reconciliation/migration_exceptions.csv"
OUTPUT_FILE = "reconciliation/migration_exceptions.csv"


def load_exceptions():
    """Load all migration exceptions from CSV."""

    with open(
        INPUT_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)


def save_exceptions(exceptions):
    """Save updated exceptions back to CSV."""

    fieldnames = [
        "Exception_ID",
        "Entity",
        "Record_ID",
        "Field",
        "Source_Value",
        "Target_Value",
        "Exception_Type",
        "Severity",
        "Status",
        "Owner",
        "Root_Cause",
        "Resolution"
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(exceptions)


def display_exceptions(exceptions):
    """Display all open exceptions."""

    print()
    print("=" * 80)
    print("             OPEN MIGRATION EXCEPTIONS")
    print("=" * 80)

    open_count = 0

    for exception in exceptions:

        if exception["Status"] == "OPEN":

            open_count += 1

            print()
            print(f"Exception ID : {exception['Exception_ID']}")
            print(f"Entity       : {exception['Entity']}")
            print(f"Record ID    : {exception['Record_ID']}")
            print(f"Field        : {exception['Field']}")
            print(f"Source Value : {exception['Source_Value']}")
            print(f"Target Value : {exception['Target_Value']}")
            print(f"Type         : {exception['Exception_Type']}")
            print(f"Severity     : {exception['Severity']}")
            print(f"Status       : {exception['Status']}")
            print("-" * 80)

    print()
    print(f"Total Open Exceptions : {open_count}")
    print("=" * 80)


def resolve_exception(exceptions):

    exception_id = input(
        "\nEnter Exception ID to resolve: "
    ).strip()

    found = False

    for exception in exceptions:

        if exception["Exception_ID"] == exception_id:

            found = True

            print()
            print("=" * 60)
            print("           EXCEPTION DETAILS")
            print("=" * 60)

            print(
                f"Exception ID : {exception['Exception_ID']}"
            )

            print(
                f"Entity       : {exception['Entity']}"
            )

            print(
                f"Record ID    : {exception['Record_ID']}"
            )

            print(
                f"Field        : {exception['Field']}"
            )

            print(
                f"Source Value : {exception['Source_Value']}"
            )

            print(
                f"Target Value : {exception['Target_Value']}"
            )

            print(
                f"Severity     : {exception['Severity']}"
            )

            print(
                f"Current Status : {exception['Status']}"
            )

            print("=" * 60)

            if exception["Status"] == "RESOLVED":

                print("\nThis exception is already RESOLVED.")
                return

            owner = input(
                "Enter Owner: "
            ).strip()

            root_cause = input(
                "Enter Root Cause: "
            ).strip()

            resolution = input(
                "Enter Resolution: "
            ).strip()

            exception["Owner"] = owner
            exception["Root_Cause"] = root_cause
            exception["Resolution"] = resolution
            exception["Status"] = "RESOLVED"

            break

    if not found:

        print()
        print(
            f"Exception ID not found: {exception_id}"
        )

        return

    save_exceptions(exceptions)

    print()
    print("=" * 60)
    print("       EXCEPTION RESOLVED SUCCESSFULLY")
    print("=" * 60)
    print(f"Exception ID : {exception_id}")
    print("Status       : RESOLVED")
    print(f"Owner        : {owner}")
    print(f"Root Cause   : {root_cause}")
    print(f"Resolution   : {resolution}")
    print("=" * 60)


def generate_summary(exceptions):

    total = len(exceptions)

    open_count = sum(
        1
        for exception in exceptions
        if exception["Status"] == "OPEN"
    )

    resolved_count = sum(
        1
        for exception in exceptions
        if exception["Status"] == "RESOLVED"
    )

    print()
    print("=" * 60)
    print("        EXCEPTION MANAGEMENT SUMMARY")
    print("=" * 60)

    print(
        f"{'Total Exceptions':<30}: {total}"
    )

    print(
        f"{'Open Exceptions':<30}: {open_count}"
    )

    print(
        f"{'Resolved Exceptions':<30}: {resolved_count}"
    )

    print("-" * 60)

    if open_count == 0:
        print(
            f"{'Exception Status':<30}: ALL RESOLVED"
        )
    else:
        print(
            f"{'Exception Status':<30}: OPEN ITEMS REMAIN"
        )

    print("=" * 60)


def main():

    if not os.path.exists(INPUT_FILE):

        print(
            f"ERROR: File not found: {INPUT_FILE}"
        )

        return

    exceptions = load_exceptions()

    print()
    print("=" * 60)
    print("       MIGRATION EXCEPTION MANAGER")
    print("=" * 60)

    display_exceptions(exceptions)

    print()
    print("Options:")
    print("1. Resolve an Exception")
    print("2. Exit")

    choice = input(
        "\nEnter your choice: "
    ).strip()

    if choice == "1":

        resolve_exception(exceptions)

        # Reload after update
        exceptions = load_exceptions()

        generate_summary(exceptions)

    elif choice == "2":

        print("\nExiting Exception Manager.")

    else:

        print("\nInvalid choice.")


if __name__ == "__main__":
    main()