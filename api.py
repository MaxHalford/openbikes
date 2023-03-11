import json
from fastapi import FastAPI
import adapters

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/stations/{city}")
async def get_stations(city):
    adapter = adapters.city_adapters[city]
    with open(f"openbikes-data.git/stations/{city}.json") as f:
        raw = json.load(f)
    return [adapter(r).to_dict() for r in raw]
