import os

import groupy
import yaml

from ._config import DATA_DIR

_MANUAL_FILENAME = os.path.join(DATA_DIR, "members.yaml")
_AUTO_FILENAME = os.path.join(DATA_DIR, "members-generated.yaml")


def get_member_name(user_id):
    filename = _MANUAL_FILENAME if os.path.isfile(_MANUAL_FILENAME) else _AUTO_FILENAME
    try:
        with open(filename, "r") as members_file:
            members = yaml.load(members_file)
            for member in members["members"]:
                if member["user_id"] == user_id:
                    return member["nickname"]
    except FileNotFoundError:
        for member in groupy.Member.list():
            if user_id == member.user_id:
                return member.nickname
    raise RuntimeError("Could not find user_id '%s'" % user_id)


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
