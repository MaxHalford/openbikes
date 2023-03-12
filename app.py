import flag
import json
import pathlib
import statistics
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import adapters
import tools
import pycountry

app = FastAPI()
templates = Jinja2Templates(directory="templates")


city_countries = {
    **{city["city"]: city["country"] for city in tools.gbfs_apis},
    "brisbane": "au",
    "bruxelles": "be",
    "namur": "be",
    "santander": "es",
    "amiens": "fr",
    "cergy-pontoise": "fr",
    "creteil": "fr",
    "lyon": "fr",
    "marseille": "fr",
    "mulhouse": "fr",
    "nancy": "fr",
    "nantes": "fr",
    "rouen": "fr",
    "toulouse": "fr",
    "dublin": "ie",
    "toyama": "jp",
    "vilnius": "lt",
    "luxembourg": "lu",
    "lillestrom": "no",
    "besancon": "fr",
    "maribor": "si",
    "seville": "es",
    "valence": "es",
    "lund": "se",
    "stockholm": "se",
    "ljubljana": "si",
    "chattanooga": "us",
    "dubai": "ae",
    "vancouver": "ca",
    "rio-de-janeiro": "br",
}


@app.get("/")
async def root(request: Request):
    cities = [
        {
            "slug": city,
            "city": {"rio-de-janeiro": "Rio de Janeiro"}.get(city, city.title()),
            "country": pycountry.countries.lookup(city_countries[city].upper()).name,
            "flag": flag.flag(city_countries[city]),
        }
        for city in tools.list_cities()
    ]
    cities = sorted(cities, key=lambda c: (c["country"], c["city"]))
    for i, city in enumerate(cities, start=1):
        city["number"] = str(i).zfill(3)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "cities": cities},
    )


@app.get("/latest/{city}")
async def latest(city):
    adapter = adapters.city_adapters[city]
    with open(f"openbikes-data.git/stations/{city}.json") as f:
        raw = json.load(f)
    return [adapter(r).to_dict() for r in raw]
