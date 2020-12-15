# Standard Library Imports
import matplotlib.pyplot as plt

# Local Imports
import database as db

# ============================================================ BUILDING PLOTS ============================================================
def display_popular_titles(result_size=10):
    titles_usage_data = db.get_title_usage()[:result_size]
    titles, usage_data = [datum[0] for datum in titles_usage_data], [datum[1] for datum in titles_usage_data]

    new_figure = plt.figure()
    bar_graph = new_figure.add_subplot(1,1,1)
    plt.title("This is the title right?")

    bar_graph.bar(titles, usage_data)

    plt.xticks(
        rotation=45, 
        horizontalalignment='right',
        fontweight='light',
        fontsize='x-small'  
    )

    plt.tight_layout()
    return new_figure

my_figure = display_popular_titles()
plt.show()