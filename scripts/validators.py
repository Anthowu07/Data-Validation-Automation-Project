import pandas as pd
import logging

def validate_null_emails(df):
    null_emails = df[df["email"].isnull()]
    count = len(null_emails)
    logging.info(f"Null email check completed. Nulls found: {count}")
    return null_emails

def validate_invalid_statuses(df):
    invalid_statuses = df[~df["status"].isin(["success", "pending", "failed"])]
    count = len(invalid_statuses)
    logging.info(f"Invalid statuses check completed. Invalid statuses found: {count}")
    return invalid_statuses

def validate_user_links(txn_df, users_df):
    transactions_with_unknown_users = txn_df[~txn_df['user_id'].isin(users_df['user_id'])]
    count = len(transactions_with_unknown_users)
    logging.info(f"User Links check completed. Transactions with unknown users found: {count}")
    return transactions_with_unknown_users