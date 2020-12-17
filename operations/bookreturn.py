# Local Imports
from system_data import database as db

# ===================== Functionality for Returning Books ====================
def return_handler(selected_records):
    """
    PARAMETERS
        * selected_records -> a list of dictionaries that represent information about books on loan
    RETURN VALUES
        * None
    WHAT DOES THIS FUNCTION DO?
        * This function returns, to the shelf, the books in the selected records
    """
    for log_id, book_id in selected_records:
        db.return_book(log_id, book_id)