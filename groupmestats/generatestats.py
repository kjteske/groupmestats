import argparse
import webbrowser

from .groupserializer import GroupSerializer
from .statistic import all_statistics
from .statistics import *

def gstat_stats():
    parser = argparse.ArgumentParser(description="Generates stats for a group")
    parser.add_argument("-g", "--group", dest="group_name", required=True,
                        help="Group to generate stats for.")
    args = parser.parse_args()

    (group, messages) = GroupSerializer.load(args.group_name)

    stats = [stat_class() for name, stat_class in all_statistics.items()]
    for stat in stats:
        stat.calculate(group, messages)
    for stat in stats:
        output_html_filename = stat.show()
        try:
            webbrowser.open_new_tab(output_html_filename)
        except:
            pass
