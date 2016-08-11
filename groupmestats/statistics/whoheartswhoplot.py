import os

from plotly.graph_objs import Bar, Figure, Layout, Scatter

from ..memberlookup import message_to_author, id_to_name
from ..statistic import statistic
from ..plotly_helpers import marker, try_saving_plotly_figure

def average(the_list):
    return float(sum(the_list)) / len(the_list)

def remove_user_id_keys(id_to_foo_dict, ignore_users):
    ids_to_del = []
    for user_id in id_to_foo_dict.keys():
        if id_to_name(user_id) in ignore_users:
            ids_to_del.append(user_id)
    for id_to_del in ids_to_del:
        del id_to_foo_dict[id_to_del]

class Author(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.num_messages = 0
        self.hearter_id_to_count = {}
        self.name = id_to_name(user_id)

    def set_hearter_ids(self, hearter_ids):
        for hearter_id in hearter_ids:
            self.hearter_id_to_count[hearter_id] = 0

    def add_message(self, message):
        self.num_messages += 1
        for hearter_id in message.favorited_by:
            self.hearter_id_to_count[hearter_id] += 1

    def remove_ignored(self, ignore_users):
        remove_user_id_keys(self.hearter_id_to_count, ignore_users)

class Hearter(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.author_id_to_count = {}
        self.name = id_to_name(user_id)

    def set_author_ids(self, author_ids):
        for author_id in author_ids:
            self.author_id_to_count[author_id] = 0

    def add_message(self, message):
        self.author_id_to_count[message.user_id] += 1

    def remove_ignored(self, ignore_users):
        remove_user_id_keys(self.author_id_to_count, ignore_users)

@statistic
class WhoHeartsWhoPlot(object):
    def calculate(self, group, messages, ignore_users=[], **kwargs):
        self._id_to_authors = {}
        self._id_to_hearters = {}
        for member in group.members():
            user_id = member.user_id
            self._id_to_authors[user_id] = Author(user_id)
            self._id_to_hearters[user_id] = Hearter(user_id)

        author_ids = self._id_to_authors.keys()
        hearter_ids = self._id_to_hearters.keys()
        for author in self._id_to_authors.values():
            author.set_hearter_ids(hearter_ids)
        for hearter in self._id_to_hearters.values():
            hearter.set_author_ids(author_ids)

        for message in messages:
            author_id = message.user_id
            if author_id == "system": continue
            self._id_to_authors[author_id].add_message(message)
            for hearter_id in message.favorited_by:
                self._id_to_hearters[hearter_id].add_message(message)

        remove_user_id_keys(self._id_to_authors, ignore_users)
        remove_user_id_keys(self._id_to_hearters, ignore_users)
        for author in self._id_to_authors.values():
            author.remove_ignored(ignore_users)
        for hearter in self._id_to_hearters.values():
            hearter.remove_ignored(ignore_users)

        self._author_names = []
        for author_id in author_ids:
            author_name = id_to_name(author_id)
            if author_name not in ignore_users:
                self._author_names.append(id_to_name(author_id))
        self._author_names.sort()
        self._group_name = group.name

    def show(self):
        if not os.path.exists(self._group_name):
            os.mkdir(self._group_name)
        for hearter in self._id_to_hearters.values():
            self._plot_hearter(hearter)

    def _calc_group_percent_hearted(self, author):
        all_heart_counts = author.hearter_id_to_count.values()
        hearts_per_user = average(all_heart_counts)
        return 100 * hearts_per_user / author.num_messages

    def _plot_hearter(self, hearter):
        x_axis = self._author_names
        hearter_name = id_to_name(hearter.user_id)

        author_name_to_percent_hearted = {}
        author_name_to_group_percent_hearted = {}
        for author_id, hearts_given_to_author in hearter.author_id_to_count.items():
            author = self._id_to_authors[author_id]
            percent_hearted = 100 * float(hearts_given_to_author) / author.num_messages
            author_name_to_percent_hearted[author.name] = percent_hearted
            print("%s hearted %.1f%% (%d / %d) of %s's messages" %
                 (hearter_name, percent_hearted, hearts_given_to_author,
                  author.num_messages, author.name))

            group_percent_hearted = self._calc_group_percent_hearted(author)
            author_name_to_group_percent_hearted[author.name] = group_percent_hearted
            print("The group hearted %.1f%% of %s's messages" %
                 (group_percent_hearted, author.name))
        percent_hearted_y = []
        group_percent_hearted_y = []
        for author_name in self._author_names:
            percent_hearted_y.append(author_name_to_percent_hearted[author_name])
            group_percent_hearted_y.append(author_name_to_group_percent_hearted[author_name])

        pinkish = "#ff6699"
        darker_pinkish = "#ff0066"
        dark_blueish = "#3333cc"

        percent_hearted_bar = Bar(
            x=x_axis,
            y=percent_hearted_y,
            marker=dict(
                color=pinkish,
                line=dict(color='Red'),
            ),
            name="%s's Avg %% Hearted" % hearter_name,
            opacity=0.6,
        )
        group_percent_hearted_bar = Bar(
            x=x_axis,
            y=group_percent_hearted_y,
            marker=dict(
                color="transparent",
                line=dict(color='Blue', width=2.0),
            ),
            name="Group Avg % Hearted",
            opacity=0.6,
        )
        avg_percent_hearted = average(percent_hearted_y)
        percent_hearted_avg_line = Scatter(
            x=[x_axis[0], x_axis[-1]],
            y=[avg_percent_hearted, avg_percent_hearted],
            name="%s's Avg %% Hearted" % hearter_name,
            marker=dict(color=darker_pinkish),
        )
        group_avg_percent_hearted = average(group_percent_hearted_y)
        group_percent_hearted_avg_line = Scatter(
            x=[x_axis[0], x_axis[-1]],
            y=[group_avg_percent_hearted, group_avg_percent_hearted],
            name="Group Avg % Hearted",
            marker=dict(color=dark_blueish),
        )

        # Show what you would expect to heart for each person.
        # If the group hearts 20% of all messages, and you heart 40%,
        # then for any given author, you would expect to heart twice as many
        # of their messages as the group average.
        scale_factor = avg_percent_hearted / group_avg_percent_hearted
        expected_percent_hearted_bar = Bar(
            x=x_axis,
            y=[avg_percent * scale_factor
               for avg_percent in group_percent_hearted_y],
            marker=dict(
                color="transparent",
                line=dict(
                    color='Black',
                    width=1.0,
                ),
            ),
            name="%s's Expected Heart %%" % hearter_name,
        )
        data = [
            percent_hearted_bar,
            group_percent_hearted_bar,
            expected_percent_hearted_bar,
            percent_hearted_avg_line,
            group_percent_hearted_avg_line,
        ]
        annotations=[
            dict(x=xi, y=yi,
                 text="%.1f%%" % yi,
                 xanchor='center',
                 yanchor='bottom',
                 showarrow=False,
            ) for xi, yi in zip(x_axis, percent_hearted_y)]
        layout = Layout(
            title="%s - %s's Hearts Given" % (self._group_name, hearter_name),
            annotations=annotations,
            autosize=False,
            width=30*len(x_axis) + 300,
            height=800,
            barmode='overlay',
            yaxis=dict(title="Percent of Author's Messages Hearted"),
        )
        figure = Figure(data=data, layout=layout)
        filename = os.path.join(self._group_name, "%s - %s - Hearts Given.png" %
                                                (self._group_name, hearter_name))
        try_saving_plotly_figure(figure, filename)
