import os

import groupy
import yaml

from ._config import DATA_DIR

_MANUAL_FILENAME = os.path.join(DATA_DIR, "members.yaml")
_AUTO_FILENAME = os.path.join(DATA_DIR, "members-generated.yaml")

class MemberNotFoundError(RuntimeError): pass

class MemberLookup(object):
    def __init__(self):
        self._ids_to_name = {}
        try:
            self._load_from_file()
        except FileNotFoundError:
            self._load_from_groupy()

    def id_to_name(self, user_id):
        return self._ids_to_name[user_id]

    def _load_from_file(self):
        filename = _MANUAL_FILENAME if os.path.isfile(_MANUAL_FILENAME) else _AUTO_FILENAME
        with open(filename, "r") as members_file:
            members_yaml = yaml.load(members_file)
            for member in members_yaml["members"]:
                self._ids_to_name[member["user_id"]] = member["nickname"]

    def _load_from_groupy(self):
        for member in groupy.Member.list():
            self._ids_to_name[member.user_id] = member.nickname

_member_lookup = MemberLookup()


def id_to_name(user_id):
    return _member_lookup.id_to_name(user_id)


def message_to_author(message):
    try:
        return id_to_name(message.user_id)
    except:
        # @todo: print warning?
        return message.name


def gstat_gen_members():
    members = []
    for member in groupy.Member.list():
        members.append({
            "nickname" : member.nickname,
            "user_id" : member.user_id,
        })
    members.sort(key=lambda member: member["nickname"])
    with open(_AUTO_FILENAME, "w") as members_file:
        yaml.dump({"members" : members}, members_file)
