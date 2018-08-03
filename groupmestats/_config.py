import os

import plotly
import yaml

DATA_DIR = os.path.join(os.path.expanduser('~'), ".groupmestats")

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


GROUPME_TOKEN_FILE = os.path.join(os.path.expanduser('~'), ".groupme_key")

def get_groupme_token():
    with open(GROUPME_TOKEN_FILE, "r") as f:
        return f.readline().strip()
