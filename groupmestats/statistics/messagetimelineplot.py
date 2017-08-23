import argparse
import datetime
import operator
import os

from plotly.graph_objs import Figure, Layout, Scatter

from ..groupserializer import GroupSerializer
from ..plotly_helpers import try_saving_plotly_figure


class Stat(object):
    def __init__(self):
        self.message_count = 0
        self.heart_count = 0


def parse_args():
    parser = argparse.ArgumentParser(description="Plots timeline of messages/hearts")
    parser.add_argument("-g", "--group", dest="group_name", required=True,
                        help="Group to generate stat for.")
    args = parser.parse_args()
    return args


def get_days_to_stats(messages):
    """ Get dict of day ordinal to Stat """
    days_to_stats = {}
    min_day_ordinal = 99999999
    max_day_ordinal = 0
    for message in messages:
        day_ordinal = message.created_at.toordinal()
        max_day_ordinal = max(max_day_ordinal, day_ordinal)
        min_day_ordinal = min(min_day_ordinal, day_ordinal)
        if day_ordinal not in days_to_stats:
            days_to_stats[day_ordinal] = Stat()
        days_to_stats[day_ordinal].message_count += 1
        days_to_stats[day_ordinal].heart_count += len(message.favorited_by)

    for day_ordinal in range(min_day_ordinal, max_day_ordinal + 1):
        if day_ordinal not in days_to_stats:
            days_to_stats[day_ordinal] = Stat()
    return days_to_stats


def gstat_timeline_main():
    args = parse_args()
    print("args: %s" % str(args))

    (group, messages) = GroupSerializer.load(args.group_name)
    group.name = args.group_name

    days_to_stats = get_days_to_stats(messages)
    sorted_days_to_stats = sorted(days_to_stats.items(),
                                  key=operator.itemgetter(0))
    x_datetimes = []
    y_message_counts = []
    y_heart_counts = []
    for (ordinal, stat) in sorted_days_to_stats:
        date = datetime.date.fromordinal(ordinal)
        x_datetimes.append(date)
        y_message_counts.append(stat.message_count)
        y_heart_counts.append(stat.heart_count)

    message_count_scatter = Scatter(
        x=x_datetimes,
        y=y_message_counts,
        name="Number of messages")
    heart_count_scatter = Scatter(
        x=x_datetimes,
        y=y_heart_counts,
        name="Hearts given")
    data = [message_count_scatter, heart_count_scatter]
    one_day = 86400000.0
    layout = Layout(
        title="%s - Messages and Hearts per Day" % group.name,
        xaxis=dict(
            title="Date",
            tickmode="linear",
            tick0=x_datetimes[0],
            dtick=one_day*14,
            ),
        )
    figure = Figure(data=data, layout=layout)
    filename = os.path.join(group.name, "%s - Messages and Hearts Timeline.png"
                            % group.name)
    try_saving_plotly_figure(figure, filename)
