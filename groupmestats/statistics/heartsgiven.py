from ..memberlookup import id_to_name
from ..statistic import statistic

class RunningTotal(object):
    def __init__(self, name):
        self.name = name
        self.num_hearts_given = 0


@statistic
class HeartsGiven(object):
    def calculate(self, group, messages):
        # Don't look up name from file each time through the loop
        # because it's very slow.
        id_to_totals = {}
        for message in messages:
            for user_id in message.favorited_by:
                if user_id == "system": continue
                if user_id not in id_to_totals:
                    id_to_totals[user_id] = RunningTotal(id_to_name(user_id))
                id_to_totals[user_id].num_hearts_given += 1

        self._totals = sorted(id_to_totals.values(), reverse=True,
                              key=lambda total: total.num_hearts_given)

    def show(self):
        for total in self._totals:
            print("%20s %3u hearts given" % (total.name, total.num_hearts_given))

