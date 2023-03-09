import concurrent.futures
import logging
import json
import pathlib
import functools
import requests


def jcdecaux(city):
    api_key = "644ba49840f4c1021dfa661e67c3c9bfeb41b88e"
    url = f"https://api.jcdecaux.com/vls/v1/stations?contract={city}&apiKey={api_key}"
    r = requests.get(url)
    r.raise_for_status()
    stations = r.json()
    return sorted(stations, key=lambda x: x["number"])


def call_and_save(func, filename):
    data = func()
    filename.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, sort_keys=True, indent=4)


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

here = pathlib.Path(__file__).parent
logging.basicConfig(level="INFO", format="level=%(levelname)s %(message)s")


def main():
    cities = (pathlib.Path(__file__).parent / "cities.txt").read_text().splitlines()

    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        future_to_city = {
            executor.submit(
                call_and_save,
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


if __name__ == "__main__":
    main()
