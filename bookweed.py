# Standard Library Imports


# Local Imports
import database as db

# ============================================================ BUILDING PLOTS ============================================================
def display_popular_titles(result_size=10):
    titles_usage_data = db.get_title_usage()[:result_size]
    titles, usage_data = [datum[0] for datum in titles_usage_data], [datum[1] for datum in titles_usage_data]

display_popular_titles()