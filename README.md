# QA Data Validation Project

This project simulates data validation tasks of a QA Data Engineer using Python and SQLite.

## Features
- Checks for NULL values in `users`
- Validates transaction statuses
- Checks that each transaction has an associated user
- Reports are saved to `qa_reports/`

## Logging
All validation reports and logs will be output to the qa_reports/ folder. This folder is ignored in Git, as it contains auto-generated files.

## Setup
```bash
pip install -r requirements.txt
python scripts/validate_data.py