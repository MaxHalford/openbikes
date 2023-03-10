import argparse
import concurrent.futures
import datetime as dt
import logging
import pathlib
import functools
import requests
import os
import tools
import pygit2
import time


def jcdecaux(city):
    api_key = os.environ["JCDECAUX_API_KEY"]
    url = f"https://api.jcdecaux.com/vls/v1/stations?contract={city}&apiKey={api_key}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    stations = r.json()
    for station in stations:
        del station["last_update"]
    return sorted(stations, key=lambda x: x["number"])


def gbfs(info_url, status_url):
    r = requests.get(info_url)
    r.raise_for_status()
    information = {s["station_id"]: s for s in r.json()["data"]["stations"]}
    r = requests.get(status_url)
    r.raise_for_status()
    statuses = {s["station_id"]: s for s in r.json()["data"]["stations"]}
    stations = [
        {
            "information": information[station_id],
            "status": statuses[station_id],
        }
        for station_id in information
    ]
    for station in stations:
        del station["status"]["last_reported"]
    return stations


city_funcs = {
    **{
        city["city"]: functools.partial(
            gbfs, city["information_url"], city["status_url"]
        )
        for city in tools.gbfs_apis
    },
    **{
        city: functools.partial(jcdecaux, city) for city in tools.list_jcdecaux_cities()
    },
    "chattanooga": functools.partial(
        gbfs,
        "https://chattanooga.publicbikesystem.net/customer/gbfs/v2/en/station_information.json",
        "https://chattanooga.publicbikesystem.net/customer/gbfs/v2/en/station_status.json",
    ),
    "dubai": functools.partial(
        gbfs,
        "https://dubai.publicbikesystem.net/customer/gbfs/v2/en/station_information.json",
        "https://dubai.publicbikesystem.net/customer/gbfs/v2/en/station_status.json",
    ),
    "vancouver": functools.partial(
        gbfs,
        "https://gbfs.hopr.city/api/gbfs/13/station_information",
        "https://gbfs.hopr.city/api/gbfs/13/station_status",
    ),
    "rio-de-janeiro": functools.partial(
        gbfs,
        "https://riodejaneiro-br.publicbikesystem.net/customer/gbfs/v2/en/station_information",
        "https://riodejaneiro-br.publicbikesystem.net/customer/gbfs/v2/en/station_status",
    ),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--commit", default=False, action=argparse.BooleanOptionalAction
    )
    parser.add_argument("--push", default=False, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    here = pathlib.Path(__file__).parent
    cities = tools.list_cities()

    # Pull the latest changes from the remote
    tic = time.time()
    data_dir = here / os.environ["DATA_DIR"] / "openbikes-data"
    if not data_dir.exists():
        pygit2.clone_repository(
            "https://github.com/MaxHalford/openbikes-data", data_dir
        )
    repo = pygit2.Repository(data_dir)
    repo.remotes["origin"].fetch()
    logging.info(f"Cloned and fetched in {time.time() - tic:.0f}s")
    logging.info(f"Current size is {tools.sizeof_fmt(tools.dir_size(data_dir))}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_city = {
            executor.submit(
                tools.call_and_save,
                func=city_funcs[city],
                filename=data_dir / "stations" / f"{city}.json",
            ): city
            for city in cities
        }

    n_success = 0
    n_exceptions = 0
    for future in concurrent.futures.as_completed(future_to_city):
        city = future_to_city[future]
        try:
            future.result()
            n_success += 1
        except Exception as exc:
            logging.exception(f"{city}: {exc}")
            n_exceptions += 1
    logging.info(f"{n_success} fetched, {n_exceptions} exceptions")

    if args.commit:
        index = repo.index
        for city in cities:
            index.add(f"stations/{city}.json")
        index.write()
        ref = repo.head.name
        author = pygit2.Signature("foch47[bot]", "foch47[bot]@users.noreply.github.com")
        committer = pygit2.Signature(
            "foch47[bot]", "foch47[bot]@users.noreply.github.com"
        )
        message = f"{pathlib.Path(__file__).name} ??? {dt.datetime.now().isoformat()}"
        tree = index.write_tree()
        parents = [repo.head.target]
        repo.create_commit(ref, author, committer, message, tree, parents)
        if args.push:
            tools.push_to_origin(repo)


if __name__ == "__main__":
    main()
