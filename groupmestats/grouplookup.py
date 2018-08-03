import os

import groupy
import yaml

from ._config import DATA_DIR, get_groupme_token
from .groupmeclient import get_groupme_client

_MANUAL_FILENAME = os.path.join(DATA_DIR, "groups.yaml")
_AUTO_FILENAME = os.path.join(DATA_DIR, "groups-generated.yaml")


def get_group(group_name):
    """ Return groupy.Group """
    client = get_groupme_client()
    for group in client.groups.list():
        if group_name == group.name:
            return group
    raise RuntimeError("Could not find group '%s'" % group_name)


def get_group_id(group_name):
    filename = _MANUAL_FILENAME if os.path.isfile(_MANUAL_FILENAME) else _AUTO_FILENAME
    try:
        with open(filename, "r") as groups_file:
            groups = yaml.load(groups_file)
            for group in groups["groups"]:
                if group_name in group["names"]:
                    return group["group_id"]
    except FileNotFoundError:
        client = get_groupme_client()
        for group in client.groups.list():
            if group_name == group.name:
                return group.group_id
    raise RuntimeError("Could not find group '%s'" % group_name)


def gstat_gen_groups():
    groups = []
    client = get_groupme_client()
    for group in client.groups.list():
        groups.append({
            "group_id" : group.group_id,
            "names" : [group.name],
            })
    groups.sort(key=lambda group: group["names"][0])
    with open(_AUTO_FILENAME, "w") as groups_file:
        yaml.dump({"groups" : groups}, groups_file)
