from dataclasses import dataclass

import requests
from OSMPythonTools.nominatim import Nominatim

overpass_url = "https://overpass-api.de/api/interpreter"


@dataclass
class LatLong:
    lat: float
    long: float
    name: str = ""
    display_name: str = ""

    def __repr__(self):
        return f"LatLong(lat={self.lat}, long={self.long}, name='{self.name}')"


class OSMData:
    def __init__(self, elements: list[dict]):
        self.elements = elements
        self.node_by_id = {element["id"]: element for element in elements if element["type"] == "node"}
        self.min_lat = self._min_lat()
        self.max_lat = self._max_lat()
        self.min_lon = self._min_lon()
        self.max_lon = self._max_lon()

    def __repr__(self):
        return f"OSMData(elements={self.elements[:2]})"

    def nodes(self) -> list[dict]:
        return self.node_by_id.values()

    def ways(self) -> list[dict]:
        return [element for element in self.elements if element["type"] == "way"]

    def latitudes(self) -> list[float]:
        return [node["lat"] for node in self.nodes()]

    def longitudes(self) -> list[float]:
        return [node["lon"] for node in self.nodes()]

    def _min_lat(self) -> float:
        if not self.latitudes():
            print("Empty latitudes")
            return 0.0
        return min(self.latitudes())

    def _max_lat(self) -> float:
        if not self.latitudes():
            print("Empty latitudes")
            return 0.0
        return max(self.latitudes())

    def _min_lon(self) -> float:
        if not self.longitudes():
            print("Empty longitudes")
            return 0.0
        return min(self.longitudes())

    def _max_lon(self) -> float:
        if not self.longitudes():
            print("Empty longitudes")
            return 0.0
        return max(self.longitudes())


def overpass_query(query: str) -> OSMData:
    response = requests.get(overpass_url, params={"data": query})
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")
    data = response.json()
    return OSMData(data["elements"])


def lat_long_by_name(name: str) -> LatLong:
    nominatim = Nominatim()
    result = nominatim.query(name).toJSON()
    if not len(result):
        return LatLong(lat=0, long=0, name="Null island")
    return LatLong(
        lat=float(result[0]["lat"]), long=float(result[0]["lon"]), name=name, display_name=result[0]["display_name"]
    )


def way_details_from_name(origin: str) -> tuple[LatLong, OSMData]:
    lat_long = lat_long_by_name(origin)
    query = f"""
    [timeout:900][out:json];
    (
        way[highway](around:1000, {lat_long.lat}, {lat_long.long});
        node(w);
    );
    out body;
    """
    return lat_long, overpass_query(query)


if __name__ == "__main__":
    origin, data = way_details_from_name("Vrolikstraat 186-3")
    print(origin)
    print(data)
