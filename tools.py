import json
import pathlib
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


here = pathlib.Path(__file__).parent
with open(here / "gbfs_apis.json") as f:
    gbfs_apis = json.load(f)


def list_jcdecaux_cities():
    return {
        "brisbane",
        "bruxelles",
        "namur",
        "santander",
        "amiens",
        "cergy-pontoise",
        "creteil",
        "lyon",
        "marseille",
        "mulhouse",
        "nancy",
        "nantes",
        "rouen",
        "toulouse",
        "dublin",
        "toyama",
        "vilnius",
        "luxembourg",
        "lillestrom",
        "besancon",
        "maribor",
        "seville",
        "valence",
        "lund",
        "stockholm",
        "ljubljana",
    }


def list_cities():
    cities = list_jcdecaux_cities()
    cities |= {gbfs_api["city"] for gbfs_api in gbfs_apis[:100]}
    cities |= {"vancouver", "chattanooga", "dubai", "rio-de-janeiro"}
    return cities


def dir_size(directory):
    return sum(f.stat().st_size for f in directory.glob("**/*") if f.is_file())


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"
