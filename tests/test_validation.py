import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.validators import validate_null_emails, validate_invalid_statuses, validate_user_links

# Validates that the validate_null_emails function works as intended
def test_validate_null_emails():
    df = pd.DataFrame({
        "user_id": [1, 2],
        "email": ["a@example.com", None]
    })
    result = validate_null_emails(df)
    assert len(result) == 1

# Validates that the validate_invalid_statuses function works as intended
def test_validate_invalid_statuses():
    df = pd.DataFrame({
        "id": [1, 2], 
        "status": ["success", "invalid"]
    })
    result = validate_invalid_statuses(df)
    assert len(result) == 1
    
# Validates that the validate_user_links functions works as intended
def test_validate_user_links():
    txn_df = pd.DataFrame({
        "txn_id": [1, 2, 3],
        "user_id": [1, 1, 3],
        "status": ["success", "invalid", "pending"]
    })
    user_df = pd.DataFrame({
        "user_id": [1],
        "email": ["a@example.com"]
    })
    result = validate_user_links(txn_df, user_df)
    assert len(result) == 1
