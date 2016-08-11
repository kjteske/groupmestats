import os

from plotly.graph_objs import Bar, Figure, Layout

from ..memberlookup import message_to_author, id_to_name
from ..statistic import statistic
from ..plotly_helpers import marker, try_saving_plotly_figure


class Total(object):
    def __init__(self, author):
        self.author = author
        self.num_messages = 0
        self.hearts_received = 0

    def add_message(self, message):
        self.num_messages += 1
        self.hearts_received += len(message.favorited_by)

    def average(self):
        return float(self.hearts_received) / self.num_messages


@statistic
class HeartsPerMessage(object):
    def calculate(self, group, messages, ignore_users=[], **kwargs):
        id_to_totals = {}
        for message in messages:
            user_id = message.user_id
            if user_id == "system": continue
            if user_id not in id_to_totals:
                id_to_totals[user_id] = Total(message_to_author(message))
            id_to_totals[user_id].add_message(message)

        totals = sorted(id_to_totals.values(),
                        key=lambda total: total.author)
        self._totals = [total for total in totals
                        if total.author not in ignore_users]
        self._group_name = group.name

    def show(self):
        totals = sorted(self._totals, reverse=True,
                        key=lambda total: total.average())
        for total in totals:
            print("%20s %.2f hearts/message (%4d hearts / %3d messages)" %
                 (total.author, total.average(),
                  total.hearts_received, total.num_messages))

@statistic
class HeartsPerMessagePlot(HeartsPerMessage):
    def show(self):
        if not os.path.exists(self._group_name):
            os.mkdir(self._group_name)

        x_axis = [total.author for total in self._totals]
        y_axis = [total.average() for total in self._totals]
        hearts_per_message = Bar(
            x=x_axis,
            y=y_axis,
            marker=marker,
        )
        data = [hearts_per_message]
        layout = Layout(
            title="%s - Hearts Per Message" % self._group_name,
            autosize=False,
            width=30*len(x_axis) + 300,
            height=800,
            showlegend=False,
            annotations=[
                dict(x=xi, y=yi,
                     text="%.3f" % yi,
                     xanchor='center',
                     yanchor='bottom',
                     showarrow=False,
                ) for xi, yi in zip(x_axis, y_axis)]
        )
        figure = Figure(data=data, layout=layout)
        filename = os.path.join(self._group_name, "%s - Hearts Per Message.png"
                                                   % self._group_name)
        try_saving_plotly_figure(figure, filename)
