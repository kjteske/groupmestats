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
    def calculate(self, group, messages):
        # Don't look up author from file each time through the loop
        # because it's very slow.
        id_to_totals = {}
        for message in messages:
            user_id = message.user_id
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

