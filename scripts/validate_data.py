import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../db/qa_project.db")
REPORTS_DIR = os.path.join(BASE_DIR, "../qa_reports")

conn = sqlite3.connect(DB_PATH)

# Check for NULL emails
users_df = pd.read_sql_query("SELECT * FROM users", conn)
null_emails = users_df[users_df['email'].isnull()]
if not null_emails.empty:
    null_emails.to_csv(os.path.join(REPORTS_DIR, "null_emails.csv"), index=False)
    print("Found users with missing email addresses.")

# Check for invalid transaction statuses
txn_df = pd.read_sql_query("SELECT * FROM transactions", conn)
invalid_statuses = txn_df[~txn_df['status'].isin(['success', 'pending', 'failed'])]
if not invalid_statuses.empty:
    invalid_statuses.to_csv(os.path.join(REPORTS_DIR, "invalid_transaction_statuses.csv"), index=False)
    print("Found invalid transaction statuses.")
    
# Checks for Transactions with Unknown Users
invalid_user_links = txn_df[~txn_df['user_id'].isin(users_df['user_id'])]
if not invalid_user_links.empty:
    invalid_user_links.to_csv(os.path.join(REPORTS_DIR, "transactions_with_unknow_users.csv"), index=False)
    print("Found transactions linked to unknown users.")

conn.close()
print("Validation checks completed.")