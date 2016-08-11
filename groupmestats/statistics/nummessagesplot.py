import os

from plotly.graph_objs import Bar, Figure, Layout

from ..memberlookup import message_to_author, id_to_name
from ..statistic import statistic
from ..plotly_helpers import marker, try_saving_plotly_figure


class Total(object):
    def __init__(self, author):
        self.author = author
        self.num_messages = 0


@statistic
class NumMessagesPlot(object):
    def calculate(self, group, messages, ignore_users=[], **kwargs):
        id_to_totals = {}
        for message in [message for message in messages
                        if message.user_id != "system"]:
            user_id = message.user_id
            if user_id not in id_to_totals:
                id_to_totals[user_id] = Total(message_to_author(message))
            id_to_totals[user_id].num_messages += 1

        totals = sorted(id_to_totals.values(),
                        key=lambda total: total.author)
        self._totals = [total for total in totals
                        if total.author not in ignore_users]
        self._group_name = group.name

    def show(self):
        if not os.path.exists(self._group_name):
            os.mkdir(self._group_name)
        x_axis = [total.author for total in self._totals]
        y_axis = [total.num_messages for total in self._totals]
        num_messages = Bar(
            x=x_axis,
            y=y_axis,
            marker=marker,
        )
        data = [num_messages]
        layout = Layout(
            title="%s - Messages Sent" % self._group_name,
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
        filename = os.path.join(self._group_name, "%s - Messages Sent.png"
                                                  % self._group_name)
        try_saving_plotly_figure(figure, filename)
