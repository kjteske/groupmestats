import argparse
import os
import pickle

from .groupmeclient import get_groupme_client
from .grouplookup import get_group_id
from ._config import DATA_DIR


def _get_all_messages(group):
    messages = [message for message in group.messages.list_all()]
    return messages


class GroupSerializer(object):
    @classmethod
    def save(cls, group):
        messages = _get_all_messages(group)
        with open(cls._group_filename(group.group_id), "wb") as group_file:
            pickle.dump(group, group_file)
        with open(cls._messages_filename(group.group_id), "wb") as messages_file:
            pickle.dump(messages, messages_file)

    @classmethod
    def load(cls, group_name):
        group_id = get_group_id(group_name)
        with open(cls._group_filename(group_id), "rb") as group_file:
            group = pickle.load(group_file)
        with open(cls._messages_filename(group_id), "rb") as messages_file:
            messages = pickle.load(messages_file)
        return (group, messages)

    @classmethod
    def _sanitize(cls, filename):
        return filename.replace("?", "_")

    @classmethod
    def _group_filename(cls, group_id):
        return os.path.join(DATA_DIR, cls._sanitize("group-%s-group" % group_id))

    @classmethod
    def _messages_filename(cls, group_id):
        return os.path.join(DATA_DIR, cls._sanitize("group-%s-messages" % group_id))


def gstat_fetch_data():
    parser = argparse.ArgumentParser(description="Fetch GroupMe data and save locally")
    parser.add_argument("--group", help="Group to save, may be specified more than once",
                        dest="groups", default=[], action="append")
    parser.add_argument("--all", help="Save all groups", action="store_true")
    parser.add_argument("--skip", help="Group to be skipped, for use with '--all', may be specified more than once", dest="skips", default=[], action="append")

    args = parser.parse_args()
    if not args.groups and not args.all:
        parser.print_help()
        raise RuntimeError("Must specify one of --group or --all")

    client = get_groupme_client()
    for group in client.groups.list():
        if group.name in args.skips:
            continue
        if args.all or group.name in args.groups:
            GroupSerializer.save(group)
