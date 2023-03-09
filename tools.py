import json
import logging


logging.basicConfig(level="INFO", format="level=%(levelname)s %(message)s")


def call_and_save(func, filename):
    data = func()
    filename.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, sort_keys=True, indent=4)
