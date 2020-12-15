# Standard Library Imports
import matplotlib.pyplot as plt

# Local Imports
import database as db

# ============================================================ BUILDING PLOTS ============================================================
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

plt.show()