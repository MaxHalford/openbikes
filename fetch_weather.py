import argparse
import concurrent.futures
import datetime as dt
import pathlib
import functools
import requests
import tools
import logging
import pygit2

with open("gbfs_apis.json") as f:
    gbfs_apis = json.load(f)

locations = {
    "brisbane": (27.4698, 153.0251),
    "bruxelles": (50.8467, 4.3525),
    "namur": (50.4667, 4.8667),
    "santander": (43.4623, -3.8044),
    "amiens": (49.8942, 2.2958),
    "cergy-pontoise": (49.0369, 2.0753),
    "creteil": (48.7833, 2.4667),
    "lyon": (45.7640, 4.8357),
    "marseille": (43.2965, 5.3698),
    "mulhouse": (47.7500, 7.3333),
    "nancy": (48.6833, 6.2000),
    "nantes": (47.2184, -1.5536),
    "rouen": (49.4432, 1.0993),
    "toulouse": (43.6045, 1.4442),
    "dublin": (53.3498, -6.2603),
    "toyama": (36.6953, 137.2114),
    "vilnius": (54.6872, 25.2797),
    "luxembourg": (49.6116, 6.1319),
    "lillestrom": (59.9548, 11.0374),
    "besancon": (47.2378, 6.0244),
    "maribor": (46.5547, 15.6467),
    "seville": (37.3891, -5.9845),
    "valence": (39.4699, -0.3774),
    "lund": (55.7031, 13.1937),
    "stockholm": (59.3293, 18.0686),
    "ljubljana": (46.0514, 14.5050),
    "chattanooga": (35.0456, -85.3097),
    "dubai": (25.2048, 55.2708),
    "vancouver": (49.2827, -123.1207),
    "rio-de-janeiro": (-22.9068, -43.1729),
}


def fetch_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,rain,windspeed_10m&forecast_days=1"
    r = requests.get(url)
    r.raise_for_status()
    weather = r.json()
    del weather["generationtime_ms"]
    return weather


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
    data_dir = here / "openbikes-data.git"
    if not data_dir.exists():
        pygit2.clone_repository(
            "https://github.com/MaxHalford/openbikes-data", data_dir
        )
    repo = pygit2.Repository(data_dir)
    repo.remotes["origin"].fetch()

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_city = {
            executor.submit(
                tools.call_and_save,
                func=functools.partial(fetch_weather, *locations[city]),
                filename=here / "openbikes-data.git" / "weather" / f"{city}.json",
            ): city
            for city in cities
        }

    for future in concurrent.futures.as_completed(future_to_city):
        city = future_to_city[future]
        try:
            future.result()
        except Exception as exc:
            logging.exception(f"{city}: {exc}")
        logging.info(f"{n_success} fetched, {n_exceptions} exceptions")

    if args.commit:
        repo = pygit2.Repository(here / "openbikes-data.git")
        index = repo.index
        for city in cities:
            index.add(f"weather/{city}.json")
        index.write()
        ref = repo.head.name
        author = pygit2.Signature("foch47[bot]", "foch47[bot]@users.noreply.github.com")
        committer = pygit2.Signature(
            "foch47[bot]", "foch47[bot]@users.noreply.github.com"
        )
        message = f"{pathlib.Path(__file__).name} — {dt.datetime.now().isoformat()}"
        tree = index.write_tree()
        parents = [repo.head.target]
        repo.create_commit(ref, author, committer, message, tree, parents)
        if args.push:
            tools.push_to_origin(repo)


if __name__ == "__main__":
    main()
