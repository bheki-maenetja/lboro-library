# Local Imports
from system_data import database as db

# =========================================================================== Functionality for Checking Out Books ===========================================================================
def checkout_handler(member_id, book_ids, loan_duration):
    for book_id in book_ids:
        db.checkout_book(book_id, member_id, loan_duration)