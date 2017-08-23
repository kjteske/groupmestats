import argparse
import os

import groupy
import yaml

from ._config import DATA_DIR
from groupmestats.grouplookup import get_group

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
    parser = argparse.ArgumentParser(description="Generates members file")
    parser.add_argument("-g", "--group", dest="group_name", required=True,
                        help="Group name")
    args = parser.parse_args()
    gstat_gen_members_for_group(args.group_name)


def gstat_gen_members_for_group(group_name):
    group = get_group(group_name)
    members = []
    for member in group.members():
        members.append({
            "nickname": member.nickname,
            "user_id": member.user_id,
        })
    members.sort(key=lambda member: member["nickname"])
    filename = os.path.join(DATA_DIR,
                            "members-generated-%s.yaml" % group.group_id)
    print("Writing members to %s" % filename)
    with open(filename, "w") as members_file:
        yaml.dump({"members": members}, members_file)
