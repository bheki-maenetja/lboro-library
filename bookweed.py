# Standard Library Imports
import matplotlib.pyplot as plt

# Local Imports
import database as db

# ============================================================ BUILDING GRAPHS ============================================================
## Book Title Graphs =========================================
def display_popular_titles(result_size=10, display_most_popular=True):
    titles_usage_data = db.get_title_usage()[:result_size] if display_most_popular else db.get_title_usage()[-result_size:]
    titles, usage_data = [datum[0] for datum in titles_usage_data], [datum[1] for datum in titles_usage_data]

    new_figure = plt.figure()
    bar_graph = new_figure.add_subplot(1,1,1)

    plt.title(f"The {result_size} {'Most' if display_most_popular else 'Least'} Popular Titles")
    
    plt.ylabel("Number of Checkouts")
    plt.xlabel("Book Titles")

    bar_graph.bar(titles, usage_data)

    plt.xticks(
        rotation=45, 
        horizontalalignment='right',
        fontweight='light',
        fontsize='x-small'  
    )

    plt.tight_layout()
    return new_figure

def display_least_popular_titles():
    return display_popular_titles(display_most_popular=False)

## Book Category Graphs ======================================
non_fiction_categories = [
    "languages",
    "philosophy",
    "technology",
    "art",
    "social",
    "sports",
    "biography"
]

fiction_categories = [
    "horror",
    "fantasy",
    "sci-fi",
    "adventure"
]

def display_popular_categories(main_category, sub_categories):
    category_usage_data = db.get_category_usage_data(main_category, sub_categories)
    category_usage_data.sort(key=lambda x: x[1], reverse=True)
    
    new_figure = plt.figure()
    bar_graph = new_figure.add_subplot(1,1,1)

    plt.title(f"Most Popular {main_category.title()} Categories")
    plt.ylabel("Number of Checkouts for Books in Category")
    plt.xlabel("Book Categories")

    bar_graph.bar(
        [datum[0] for datum in category_usage_data], 
        [datum[1] for datum in category_usage_data]
    )

    plt.xticks(
        rotation=45, 
        horizontalalignment='right',
        fontweight='light',
        fontsize='x-small'  
    )

    plt.tight_layout()
    return new_figure

def display_fiction_categories():
    return display_popular_categories("fiction", fiction_categories)

def display_nonfiction_categories():
    return display_popular_categories("non-fiction", non_fiction_categories)

## Book Usage Graphs =========================================
def display_book_usage_data():
    book_usage_data = db.get_book_usage_data()

    new_figure = plt.figure()
    bar_graph = new_figure.add_subplot(1,1,1)

    plt.title("Book Usage Over Time")
    plt.ylabel("Number of Checkouts")
    plt.xlabel("Years")

    bar_graph.bar(
        [datum[0] for datum in book_usage_data],
        [datum[1] for datum in book_usage_data]
    )

    plt.xticks(
        rotation=45, 
        horizontalalignment='right',
        fontweight='light',
        fontsize='x-small'  
    )

    plt.tight_layout()
    return new_figure

# ============================================================ UNUSED TITLES ============================================================
def get_unused_titles():
    unused_titles = sorted(db.get_unused_titles())
    return unused_titles

# ============================================================ SYSTEM INFO ============================================================
def get_system_info():
    return [
        ('Total Books:', len(db.get_all_books())),
        ('Total Unique Titles:', len(db.get_all_titles())),
        ('Books on Loan:', len(db.get_books_on_loan())),
        ('Overdue Books:', len(db.search_books_on_loan('', only_overdue=True)))
    ]

# display_popular_categories("fiction", fiction_categories)
# display_book_usage_data()
# plt.show()