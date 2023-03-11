import json
import logging
import os
import dotenv
import pygit2

dotenv.load_dotenv()

logging.basicConfig(level="INFO", format="level=%(levelname)s %(message)s")


def call_and_save(func, filename):
    data = func()
    filename.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, sort_keys=True, indent=4)


def push_to_origin(repo):
    remote = repo.remotes["origin"]
    credentials = pygit2.UserPass("MaxHalford", os.environ["GITHUB_TOKEN"])
    remote.credentials = credentials
    callbacks = pygit2.RemoteCallbacks(credentials=credentials)
    remote.push(["refs/heads/master"], callbacks=callbacks)
