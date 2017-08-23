import os

from plotly.graph_objs import Bar, Figure, Layout

from ..memberlookup import id_to_name
from ..plotly_helpers import marker, try_saving_plotly_figure
from ..statistic import statistic

class RunningTotal(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.name = id_to_name(user_id)
        self.num_hearts_given = 0


@statistic
class HeartsGiven(object):
    def calculate(self, group, messages, ignore_users=[], **kwargs):
        self._id_to_totals = {}
        for message in messages:
            for user_id in message.favorited_by:
                if user_id == "system": continue
                if id_to_name(user_id) in ignore_users: continue
                if user_id not in self._id_to_totals:
                    self._id_to_totals[user_id] = RunningTotal(user_id)
                self._id_to_totals[user_id].num_hearts_given += 1

        for member in group.members():
            user_id = member.user_id
            if user_id == "system": continue
            if id_to_name(user_id) in ignore_users: continue
            if user_id not in self._id_to_totals:
                self._id_to_totals[user_id] = RunningTotal(user_id)

        self._group_name = group.name

    def show(self):
        totals = sorted(self._id_to_totals.values(), reverse=True,
                        key=lambda total: total.num_hearts_given)
        for total in totals:
            print("%20s %3u hearts given" % (total.name, total.num_hearts_given))

@statistic
class HeartsGivenPlot(HeartsGiven):
    def show(self):
        if not os.path.exists(self._group_name):
            os.mkdir(self._group_name)

        totals = sorted(self._id_to_totals.values(), key=lambda total: total.name)
        x_axis = [total.name for total in totals]
        y_axis = [total.num_hearts_given for total in totals]
        hearts_given_bar = Bar(
            x=x_axis,
            y=y_axis,
            marker=marker,
        )
        data = [hearts_given_bar]
        layout = Layout(
            title="%s - Total Hearts Given" % self._group_name,
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
                ) for xi, yi in zip(x_axis, y_axis)],
            yaxis=dict(title="Number of Hearts"),
        )
        figure = Figure(data=data, layout=layout)
        filename = os.path.join(self._group_name, "%s - Hearts Given.png"
                                                  % self._group_name)
        try_saving_plotly_figure(figure, filename)
