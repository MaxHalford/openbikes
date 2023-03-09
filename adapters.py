import dataclasses

@dataclasses.dataclass
class Station:
    name: str
    bikes_available: int
    docks_available: int
    latitute: float
    longitude: float
    is_working: bool

    def to_dict(self):
        return dataclasses.asdict(self)

def jcdecaux(raw):
    return Station(
        name=raw["name"],
        bikes_available=raw["available_bikes"],
        docks_available=raw["available_bike_stands"],
        latitute=raw["position"]["lat"],
        longitude=raw["position"]["lng"],
        is_working=raw["status"] == "OPEN",
    )

city_adapters = {
    "brisbane": jcdecaux,
    "bruxelles": jcdecaux,
    "namur": jcdecaux,
    "santander": jcdecaux,
    "amiens": jcdecaux,
    "cergy-pontoise": jcdecaux,
    "creteil": jcdecaux,
    "lyon": jcdecaux,
    "marseille": jcdecaux,
    "mulhouse": jcdecaux,
    "nancy": jcdecaux,
    "nantes": jcdecaux,
    "rouen": jcdecaux,
    "toulouse": jcdecaux,
    "dublin": jcdecaux,
    "toyama": jcdecaux,
    "vilnius": jcdecaux,
    "luxembourg": jcdecaux,
    "lillestrom": jcdecaux,
    "besancon": jcdecaux,
    "maribor": jcdecaux,
    "seville": jcdecaux,
    "valence": jcdecaux,
    "lund": jcdecaux,
    "stockholm": jcdecaux,
    "ljubljana": jcdecaux,
}
