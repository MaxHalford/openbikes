import json
import pathlib
import statistics
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import adapters

app = FastAPI()
templates = Jinja2Templates(directory="templates")


city_countries = {
    "brisbane": "australia",
    "bruxelles": "belgium",
    "namur": "belgium",
    "santander": "spain",
    "amiens": "france",
    "cergy-pontoise": "france",
    "creteil": "france",
    "lyon": "france",
    "marseille": "france",
    "mulhouse": "france",
    "nancy": "france",
    "nantes": "france",
    "rouen": "france",
    "toulouse": "france",
    "dublin": "ireland",
    "toyama": "japan",
    "vilnius": "lithuania",
    "luxembourg": "luxembourg",
    "lillestrom": "norway",
    "besancon": "france",
    "maribor": "slovenia",
    "seville": "spain",
    "valence": "spain",
    "lund": "sweden",
    "stockholm": "sweden",
    "ljubljana": "slovenia",
}

country_flags = {
    "australia": "🇦🇺",
    "belgium": "🇧🇪",
    "spain": "🇪🇸",
    "france": "🇫🇷",
    "ireland": "🇮🇪",
    "japan": "🇯🇵",
    "lithuania": "🇱🇹",
    "luxembourg": "🇱🇺",
    "norway": "🇳🇴",
    "slovenia": "🇸🇮",
    "sweden": "🇸🇪",
}


@app.get("/")
async def root(request: Request):
    cities = [
        {
            "slug": city,
            "city": city.title(),
            "country": city_countries[city].title(),
            "flag": country_flags[city_countries[city]],
        }
        for city in (pathlib.Path(__file__).parent / "cities.txt")
        .read_text()
        .splitlines()
    ]
    cities = sorted(cities, key=lambda c: (c["country"], c["city"]))
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "cities": cities},
    )


@app.get("/live/{city}")
async def live(city):
    adapter = adapters.city_adapters[city]
    with open(f"openbikes-data.git/stations/{city}.json") as f:
        raw = json.load(f)
    return [adapter(r).to_dict() for r in raw]
