# Local Imports
from system_data import database as db

# ============================================================================= Functionality for Returning Books =============================================================================
def return_handler(selected_records):
    for log_id, book_id in selected_records:
        db.return_book(log_id, book_id)