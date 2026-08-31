import csv
import os


# =========================================================
# FILE PATHS
# =========================================================

SOURCE_CUSTOMER = "data/source/customer.csv"
TARGET_CUSTOMER = "data/target/customer.csv"

SOURCE_ACCOUNT = "data/source/account.csv"
TARGET_ACCOUNT = "data/target/account.csv"

SOURCE_TRANSACTION = "data/source/transaction.csv"
TARGET_TRANSACTION = "data/target/transaction.csv"

OUTPUT_FILE = "reconciliation/migration_exceptions.csv"


# =========================================================
# LOAD CSV DATA
# =========================================================

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


# =========================================================
# DETERMINE SEVERITY
# =========================================================

def determine_severity(exception_type, field=None):

    if exception_type == "MISSING":
        return "HIGH"

    if exception_type == "UNEXPECTED":
        return "HIGH"

    if exception_type == "FIELD_MISMATCH":

        if field == "balance":
            return "CRITICAL"

        if field == "amount":
            return "CRITICAL"

        if field == "status":
            return "HIGH"

        return "MEDIUM"

    return "MEDIUM"


# =========================================================
# COMPARE SOURCE AND TARGET
# =========================================================

def compare_entity(
    source_file,
    target_file,
    key,
    entity_name,
    exception_prefix
):

    source_data = load_data(source_file, key)
    target_data = load_data(target_file, key)

    exceptions = []

    counter = 1


    # -------------------------------------------------------
    # CHECK MISSING RECORDS
    # -------------------------------------------------------

    for record_id, source_record in source_data.items():

        if record_id not in target_data:

            exceptions.append({

                "Exception_ID":
                    f"{exception_prefix}-{counter:03d}",

                "Entity":
                    entity_name,

                "Record_ID":
                    record_id,

                "Field":
                    "",

                "Source_Value":
                    "",

                "Target_Value":
                    "",

                "Exception_Type":
                    "MISSING",

                "Severity":
                    "HIGH",

                "Status":
                    "OPEN",

                "Owner":
                    "Migration Team",

                "Root_Cause":
                    "Record missing in target system",

                "Resolution":
                    "Pending investigation"

            })

            counter += 1

            continue


        # ---------------------------------------------------
        # CHECK FIELD MISMATCHES
        # ---------------------------------------------------

        target_record = target_data[record_id]

        for field in source_record:

            if field == key:
                continue

            if source_record[field] != target_record[field]:

                exceptions.append({

                    "Exception_ID":
                        f"{exception_prefix}-{counter:03d}",

                    "Entity":
                        entity_name,

                    "Record_ID":
                        record_id,

                    "Field":
                        field,

                    "Source_Value":
                        source_record[field],

                    "Target_Value":
                        target_record[field],

                    "Exception_Type":
                        "FIELD_MISMATCH",

                    "Severity":
                        determine_severity(
                            "FIELD_MISMATCH",
                            field
                        ),

                    "Status":
                        "OPEN",

                    "Owner":
                        "Migration Team",

                    "Root_Cause":
                        "Source and target values do not match",

                    "Resolution":
                        "Pending investigation"

                })

                counter += 1


    # -------------------------------------------------------
    # CHECK UNEXPECTED RECORDS
    # -------------------------------------------------------

    for record_id in target_data:

        if record_id not in source_data:

            exceptions.append({

                "Exception_ID":
                    f"{exception_prefix}-{counter:03d}",

                "Entity":
                    entity_name,

                "Record_ID":
                    record_id,

                "Field":
                    "",

                "Source_Value":
                    "",

                "Target_Value":
                    "",

                "Exception_Type":
                    "UNEXPECTED",

                "Severity":
                    "HIGH",

                "Status":
                    "OPEN",

                "Owner":
                    "Migration Team",

                "Root_Cause":
                    "Record exists in target but not in source",

                "Resolution":
                    "Pending investigation"

            })

            counter += 1


    return exceptions


# =========================================================
# GENERATE EXCEPTION FILE
# =========================================================

def generate_exception_file():

    all_exceptions = []


    # -------------------------------------------------------
    # CUSTOMER
    # -------------------------------------------------------

    all_exceptions.extend(

        compare_entity(
            SOURCE_CUSTOMER,
            TARGET_CUSTOMER,
            "customer_id",
            "Customer",
            "EXC-CUST"
        )

    )


    # -------------------------------------------------------
    # ACCOUNT
    # -------------------------------------------------------

    all_exceptions.extend(

        compare_entity(
            SOURCE_ACCOUNT,
            TARGET_ACCOUNT,
            "account_id",
            "Account",
            "EXC-ACC"
        )

    )


    # -------------------------------------------------------
    # TRANSACTION
    # -------------------------------------------------------

    all_exceptions.extend(

        compare_entity(
            SOURCE_TRANSACTION,
            TARGET_TRANSACTION,
            "transaction_id",
            "Transaction",
            "EXC-TXN"
        )

    )


    # -------------------------------------------------------
    # CREATE OUTPUT DIRECTORY
    # -------------------------------------------------------

    os.makedirs(
        "reconciliation",
        exist_ok=True
    )


    # -------------------------------------------------------
    # WRITE EXCEPTION CSV
    # -------------------------------------------------------

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(

            file,

            fieldnames=[

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

        )

        writer.writeheader()

        writer.writerows(all_exceptions)


    # -------------------------------------------------------
    # DISPLAY RESULT
    # -------------------------------------------------------

    print()
    print("========================================")
    print("     MIGRATION EXCEPTION MANAGER")
    print("========================================")
    print(
        f"Total Exceptions : {len(all_exceptions)}"
    )
    print(
        f"Output File      : {OUTPUT_FILE}"
    )
    print("========================================")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    generate_exception_file()