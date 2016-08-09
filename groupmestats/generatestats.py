import argparse
import webbrowser

from .groupserializer import GroupSerializer
from .statistic import all_statistics
from .statistics import *

def gstat_stats():
    parser = argparse.ArgumentParser(description="Generates stats for a group")
    parser.add_argument("-g", "--group", dest="group_name", required=True,
                        help="Group to generate stats for.")
    parser.add_argument("-s", "--stat", dest="stats", default=[],
                        action="append",
                        help=("Name of stat to generate. This may be specified"
                              " more than once. Choices: %s "
                              % ", ".join(all_statistics.keys())))
    parser.add_argument("--all-stats", action="store_true", default=False,
                        help="Generate all possible stats.")
    args = parser.parse_args()
    stats = [stat_class() for name, stat_class in all_statistics.items()
                                    if args.all_stats or name in args.stats]
    if not stats:
        parser.print_help()
        raise RuntimeError("Must specify a valid --stat or use --all-stats")

    (group, messages) = GroupSerializer.load(args.group_name)
    for stat in stats:
        stat.calculate(group, messages)
    for stat in stats:
        output_html_filename = stat.show()
        try:
            # webbrowser.open_new_tab(output_html_filename)
            pass
        except:
            pass
