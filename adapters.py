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
    **{city["city"]: gbfs for city in tools.gbfs_apis},
    **{city: jcdecaux for city in tools.list_jcdecaux_cities()},
    "chattanooga": gbfs,
    "dubai": gbfs,
    "vancouver": gbfs,
    "rio-de-janeiro": gbfs,
}
