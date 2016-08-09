import plotly
from plotly.graph_objs import Bar, Figure, Layout

from ..memberlookup import message_to_author
from ..statistic import statistic


class RunningTotal(object):
    def __init__(self, author):
        self.author = author
        self.num_messages = 0
        self.num_hearts = 0

    def add_message(self, message):
        self.num_messages += 1
        self.num_hearts += len(message.favorited_by)

    def average(self):
        return float(self.num_hearts) / self.num_messages


@statistic
class HeartsPerMessage(object):
    def calculate(self, group, messages, ignore_users=[], **kwargs):
        # Don't look up author from file each time through the loop
        # because it's very slow.
        id_to_totals = {}
        for message in messages:
            user_id = message.user_id
            if user_id == "system": continue
            if user_id not in id_to_totals:
                id_to_totals[user_id] = RunningTotal(message_to_author(message))
            id_to_totals[user_id].add_message(message)

        self._totals = sorted(id_to_totals.values(), reverse=True,
                              key=lambda total: total.average())

    def show(self):
        for total in self._totals:
            print("%20s %.2f hearts/message (%4d hearts / %3d messages)" %
                 (total.author, total.average(),
                  total.num_hearts, total.num_messages))

def try_saving_plotly_figure(figure, filename):
    try:
        plotly.plotly.image.save_as(figure, filename)
    except plotly.exceptions.PlotlyError as e:
        if 'The response from plotly could not be translated.'in str(e):
            print("Failed to save plotly figure. <home>/.plotly/.credentials"
                  " probably not configured correctly?")
        else:
            raise

@statistic
class HeartsPerMessagePlot(HeartsPerMessage):
    def _plot_messages_and_hearts(self):
        totals = sorted(self._totals, key=lambda total: total.author)
        x_axis = [total.author for total in totals]
        num_hearts = Bar(
            x=x_axis,
            y=[total.num_hearts for total in totals],
            name='Number of Hearts'
        )
        num_messages = Bar(
            x=x_axis,
            y=[total.num_messages for total in totals],
            name='Number of messages'
        )
        data = [num_messages, num_hearts]
        layout = Layout(barmode='group', title="Messages and Hearts by Author")
        figure = Figure(data=data, layout=layout)
        try_saving_plotly_figure(figure, "MessagesAndHearts.png")

    def _plot_average_hearts_per_message(self):
        totals = sorted(self._totals, key=lambda total: total.author)
        x_axis = [total.author for total in totals]
        hearts_per_message = Bar(
            x=x_axis,
            y=[total.average() for total in totals],
            name='Average hearts / message'
        )
        data = [hearts_per_message]
        layout = Layout(title="Hearts per Message")
        figure = Figure(data=data, layout=layout)
        try_saving_plotly_figure(figure, "HeartsPerMessage.png")

    def show(self):
        self._plot_messages_and_hearts()
        self._plot_average_hearts_per_message()
