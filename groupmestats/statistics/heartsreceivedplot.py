from plotly.graph_objs import Bar, Figure, Layout

from ..memberlookup import message_to_author, id_to_name
from ..statistic import statistic
from ..plotly_helpers import marker, try_saving_plotly_figure


class Total(object):
    def __init__(self, author):
        self.author = author
        self.hearts_received = 0

    def add_message(self, message):
        self.hearts_received += len(message.favorited_by)


@statistic
class HeartsReceivedPlot(object):
    def calculate(self, group, messages, ignore_users=[], **kwargs):
        id_to_totals = {}
        for message in messages:
            user_id = message.user_id
            if user_id not in id_to_totals:
                id_to_totals[user_id] = Total(message_to_author(message))
            id_to_totals[user_id].add_message(message)

        totals = sorted(id_to_totals.values(),
                        key=lambda total: total.author)
        self._totals = [total for total in totals
                        if total.author not in ignore_users]
        self._group_name = group.name

    def show(self):
        x_axis = [total.author for total in self._totals]
        y_axis = [total.hearts_received for total in self._totals]
        hearts_received = Bar(
            x=x_axis,
            y=y_axis,
            marker=marker,
        )
        data = [hearts_received]
        layout = Layout(
            title="Hearts Received",
            autosize=False,
            width=30*len(x_axis) + 300,
            height=800,
            showlegend=False,
            annotations=[
                dict(x=xi, y=yi,
                     text=str(yi),
                     xanchor='center',
                     yanchor='bottom',
                     showarrow=False,
                ) for xi, yi in zip(x_axis, y_axis)]
        )
        figure = Figure(data=data, layout=layout)
        try_saving_plotly_figure(figure,
                                 "%s_Hearts Received.png"
                                 % self._group_name)
