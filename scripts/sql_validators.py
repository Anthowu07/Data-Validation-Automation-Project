import sqlite3
import logging
import os

def run_sql_validations(dp_path="db/qa_project.db"):
    logging.info("=== SQL-Based Validation Started ===")
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, f"../{dp_path}")
    REPORTS_DIR = os.path.join(BASE_DIR, "../qa_reports")
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    queries = {
        "null_emails": "SELECT user_id FROM users WHERE email IS NULL",
        "invalid_statuses": "SELECT txn_id FROM transactions WHERE status NOT IN ('success', 'failed', 'pending')",
        "orphaned_transactions": """
            SELECT t.txn_id FROM transactions t
            LEFT JOIN users u ON t.user_id = u.user_id
            WHERE u.user_id IS NULL
        """
    }
    
    for check_name, sql in queries.items():
        cursor.execute(sql)
        results = cursor.fetchall()
        count = len(results)
        
        if count > 0:
            report_path = os.path.join(REPORTS_DIR, f"sql_validation_{check_name}.csv")
            with open(report_path, "w") as f:
                f.write("id\n")
                for row in results:
                    f.write(f"{row[0]}\n")
            logging.info(f"[{check_name}] Found {count} issue(s) - saved to {report_path}")
        else:
            logging.info(f"[{check_name}] No issues found.")
            
        logging.info(f"{check_name}: {len(results)} issue(s) found.")
    
    conn.close()
    logging.info("=== SQL-Based Validation Complete ===\n")