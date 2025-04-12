from textwrap import dedent

import svg
from tqdm import tqdm

from src.map_api import way_details_from_name


def latlon_to_point(lat, lon, min_lat, max_lat, min_lon, max_lon, width, height) -> tuple[int, int]:
    x = (lon - min_lon) / (max_lon - min_lon) * width
    y = height - (lat - min_lat) / (max_lat - min_lat) * height
    return x, y


def render(name: str, width: int, height: int) -> svg.SVG:
    origin, data = way_details_from_name(name)

    elements = [
        svg.Style(
            text=dedent(
                """
                    .small { font: 13px sans-serif; }

                    /* Note that the color of the text is set with the    *
                    * fill property, the color property is for HTML only */
                    .Rrrrr { font: italic 40px serif; fill: red; }
                """
            ),
        )
    ]
    for way in tqdm(data.ways()):
        for i in range(len(way["nodes"]) - 1):
            node1 = data.node_by_id.get(way["nodes"][i])
            node2 = data.node_by_id.get(way["nodes"][i + 1])
            x1, y1 = latlon_to_point(
                node1["lat"],
                node1["lon"],
                data.min_lat,
                data.max_lat,
                data.min_lon,
                data.max_lon,
                width,
                height,
            )
            x2, y2 = latlon_to_point(
                node2["lat"],
                node2["lon"],
                data.min_lat,
                data.max_lat,
                data.min_lon,
                data.max_lon,
                width,
                height,
            )
            elements.append(svg.Line(x1=x1, y1=y1, x2=x2, y2=y2, stroke="black", stroke_width=2))
    x, y = latlon_to_point(
        origin.lat, origin.long, data.min_lat, data.max_lat, data.min_lon, data.max_lon, width, height
    )
    elements.append(svg.Circle(cx=x, cy=y, r=3, fill="red", class_="small", stroke="red", stroke_width=3))
    elements.append(svg.Text(x=x - 20, y=y + 20, class_=["small"], text=origin.name, fill="red"))
    doc = svg.SVG(width=width, height=height, elements=elements)

    return doc


def to_svg(doc: svg.SVG, filename: str) -> str:
    with open(filename, "w") as f:
        f.write(str(doc))
    return str(doc)


if __name__ == "__main__":
    to_svg(render("Ceintuurbaan 364", 2400, 1800), "ceintuurbaan.svg")
