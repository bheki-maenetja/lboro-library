# Local Imports
from system_data import database as db

# =================== Functionality for Checking Out Books ===================
def checkout_handler(member_id, book_ids, loan_duration):
    """
    PARAMETERS
        * member_id -> an integer representing the unique id of a library member
        * book_ids -> a list of integers that represent the unique ids of selected books
        * loan_duration -> an integer representing the number of days that the selected books will be loaned out for
    RETURN VALUES
        * None
    WHAT DOES THIS FUNCTION DO?
        * This function loans out the selected books for the given loan_duration
    """
    for book_id in book_ids:
        db.checkout_book(book_id, member_id, loan_duration)