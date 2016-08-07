all_statistics = {}

def statistic(cls):
    """ Class decorator for statistics

    Your decorated class should define these methods:
        calculate(self, group, messages)
        show(self)
    """
    all_statistics[cls.__name__] = cls
    return cls
