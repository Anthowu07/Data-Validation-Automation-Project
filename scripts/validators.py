import pandas as pd

def validate_null_emails(df):
    return df[df["email"].isnull()]

def validate_invalid_statuses(df):
    return df[~df["status"].isin(["success", "pending", "failed"])]

def validate_user_links(txn_df, users_df):
    return txn_df[~txn_df['user_id'].isin(users_df['user_id'])]