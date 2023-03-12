import dataclasses
import tools


@dataclasses.dataclass
class Station:
    name: str
    bikes_available: int
    docks_available: int
    latitude: float
    longitude: float
    is_working: bool

    def to_dict(self):
        return dataclasses.asdict(self)


def brisbane(raw):
    return Station(
        name=raw["name"],
        bikes_available=raw["num_bikes_available"],
        docks_available=raw["num_docks_available"],
        latitude=raw["lat"],
        longitude=raw["lon"],
        is_working=raw["is_installed"] == 1 and raw["is_renting"] == 1,
    )


def jcdecaux(raw):
    return Station(
        name=raw["name"],
        bikes_available=raw["available_bikes"],
        docks_available=raw["available_bike_stands"],
        latitude=raw["position"]["lat"],
        longitude=raw["position"]["lng"],
        is_working=raw["status"] == "OPEN",
    )


def gbfs(raw):
    return Station(
        name=raw["information"]["name"],
        bikes_available=raw["status"]["num_bikes_available"],
        docks_available=raw["status"]["num_docks_available"],
        latitude=raw["information"]["lat"],
        longitude=raw["information"]["lon"],
        is_working=bool(raw["information"]["is_renting"]),
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
    "chattanooga": gbfs,
    "dubai": gbfs,
    "vancouver": gbfs,
    "rio-de-janeiro": gbfs,
}
