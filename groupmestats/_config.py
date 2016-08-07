import os

DATA_DIR = os.path.join(os.path.expanduser('~'), ".groupmestats")

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
