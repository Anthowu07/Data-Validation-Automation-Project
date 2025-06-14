import sqlite3
import pandas as pd
import os
import sys
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.validators import validate_null_emails, validate_invalid_statuses, validate_user_links
from scripts.sql_validators import run_sql_validations

logging.basicConfig(
    filename="qa_reports/logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../db/qa_project.db")
REPORTS_DIR = os.path.join(BASE_DIR, "../qa_reports")

os.makedirs(REPORTS_DIR, exist_ok=True)

def main():
    logging.info("=== Python-Based Validation Started ===")
    conn = sqlite3.connect(DB_PATH)

    users_df = pd.read_sql_query("SELECT * FROM users", conn)
    txn_df = pd.read_sql_query("SELECT * FROM transactions", conn)

    # Check for NULL emails
    null_emails = validate_null_emails(users_df)
    if not null_emails.empty:
        null_emails.to_csv(os.path.join(REPORTS_DIR, "python_validation_null_emails.csv"), index=False)
        logging.info("Check completed: Null emails")
    else:
        logging.info("[Null Emails] No issues found.")

    # Check for invalid transaction statuses
    invalid_statuses = validate_invalid_statuses(txn_df)
    if not invalid_statuses.empty:
        invalid_statuses.to_csv(os.path.join(REPORTS_DIR, "python_validation_invalid_transaction_statuses.csv"), index=False)
        logging.info("Check completed: Invalid statuses")
    else:
        logging.info("[Invalid Statuses] No issues found.")
        
    # Checks for Transactions with Unknown Users
    invalid_user_links = validate_user_links(txn_df, users_df)
    if not invalid_user_links.empty:
        invalid_user_links.to_csv(os.path.join(REPORTS_DIR, "python_validation_transactions_with_unknown_users.csv"), index=False)
        logging.info("Check completed: Invalid user links")
    else:
        logging.info("[Unknown User Links] No issues found.")
        
    conn.close()
    logging.info("=== Python-Based Validation Complete ===\n")
    
    run_sql_validations()
    
if __name__ == "__main__":
    main()

