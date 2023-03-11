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


def jcdecaux(city):
    api_key = os.environ["JCDECAUX_API_KEY"]
    url = f"https://api.jcdecaux.com/vls/v1/stations?contract={city}&apiKey={api_key}"
    r = requests.get(url)
    r.raise_for_status()
    stations = r.json()
    for station in stations:
        del station["last_update"]
    return sorted(stations, key=lambda x: x["number"])


city_funcs = {
    "brisbane": functools.partial(jcdecaux, "brisbane"),
    "bruxelles": functools.partial(jcdecaux, "bruxelles"),
    "namur": functools.partial(jcdecaux, "namur"),
    "santander": functools.partial(jcdecaux, "santander"),
    "amiens": functools.partial(jcdecaux, "amiens"),
    "cergy-pontoise": functools.partial(jcdecaux, "cergy-pontoise"),
    "creteil": functools.partial(jcdecaux, "creteil"),
    "lyon": functools.partial(jcdecaux, "lyon"),
    "marseille": functools.partial(jcdecaux, "marseille"),
    "mulhouse": functools.partial(jcdecaux, "mulhouse"),
    "nancy": functools.partial(jcdecaux, "nancy"),
    "nantes": functools.partial(jcdecaux, "nantes"),
    "rouen": functools.partial(jcdecaux, "rouen"),
    "toulouse": functools.partial(jcdecaux, "toulouse"),
    "dublin": functools.partial(jcdecaux, "dublin"),
    "toyama": functools.partial(jcdecaux, "toyama"),
    "vilnius": functools.partial(jcdecaux, "vilnius"),
    "luxembourg": functools.partial(jcdecaux, "luxembourg"),
    "lillestrom": functools.partial(jcdecaux, "lillestrom"),
    "besancon": functools.partial(jcdecaux, "besancon"),
    "maribor": functools.partial(jcdecaux, "maribor"),
    "seville": functools.partial(jcdecaux, "seville"),
    "valence": functools.partial(jcdecaux, "valence"),
    "lund": functools.partial(jcdecaux, "lund"),
    "stockholm": functools.partial(jcdecaux, "stockholm"),
    "ljubljana": functools.partial(jcdecaux, "ljubljana"),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--commit", default=False, action=argparse.BooleanOptionalAction
    )
    parser.add_argument("--push", default=False, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    here = pathlib.Path(__file__).parent
    cities = (pathlib.Path(__file__).parent / "cities.txt").read_text().splitlines()

    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        future_to_city = {
            executor.submit(
                tools.call_and_save,
                func=city_funcs[city],
                filename=here / "data" / "stations" / f"{city}.json",
            ): city
            for city in cities
        }

    for future in concurrent.futures.as_completed(future_to_city):
        city = future_to_city[future]
        try:
            future.result()
            logging.info(f"✅ {city}")
        except Exception as exc:
            logging.exception(f"❌ {city}: {exc}")

    if args.commit:
        repo = pygit2.Repository(here)
        index = repo.index
        for city in cities:
            index.add((here / "data" / "stations" / f"{city}.json").relative_to(here))
        index.write()
        ref = "HEAD"
        author = pygit2.Signature("foch47", "foch47@authors.tld")
        committer = pygit2.Signature("foch47", "foch47@committers.tld")
        message = f"{pathlib.Path(__file__).name} — {dt.datetime.now().isoformat()}"
        tree = index.write_tree()
        parents = []
        repo.create_commit(ref, author, committer, message, tree, parents)
        if args.push:
            origin = repo.remote(name="origin")
            origin.push()


if __name__ == "__main__":
    main()
