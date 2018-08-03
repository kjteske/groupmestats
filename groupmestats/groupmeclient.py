import groupy

from ._config import get_groupme_token

_client = None


def get_groupme_client():
    global _client
    if _client is None:
        _client = groupy.Client.from_token(get_groupme_token())
    return _client
