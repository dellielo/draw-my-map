""" flask_example.py

    Required packages:
    - flask
    - folium

    Usage:

    Start the flask server by running:

        $ python flask_example.py

    And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""

from flask import Flask, render_template_string

import folium
from get_map import *

app = Flask(__name__)

PATH_COUNTRY = "G:\Mon Drive/Velo/Dive and Bike en Asie/all_shape.zip"
DICT_PATH_GPX = { "Bike" : ["G:\Mon Drive/Velo/Dive and Bike en Asie/GPX/", '#0F00FF'],
                    "Bus" : ["G:\Mon Drive/Velo/Dive and Bike en Asie/GPX/Car/", '#FF5733'],
                    "Train" : ["G:\Mon Drive/Velo/Dive and Bike en Asie/GPX/Train/", '#468100'],
                    "Boat" : ["G:\Mon Drive/Velo/Dive and Bike en Asie/GPX/Boat/", '#00FFFB'],
                    }


def create_map() :
    tiles_natgeo = folium.raster_layers.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}',
    name='NatGeo',
    attr='attribution')
    route_map = folium.Map(location=[13.70, 108.94], zoom_start=5, tiles=tiles_natgeo)
    
    list_country_show =[ 'Malaysia','Vietnam', 'Cambodia', 'Thailand', 'Philippines']

    route_map = draw_shape(route_map, PATH_COUNTRY, list_country_show, exclude=True)
    route_map = draw_shape(route_map, PATH_COUNTRY, list_country_show, exclude=False)
 
    for name, infos_tracks in DICT_PATH_GPX.items() :
        gpx, color = infos_tracks
        track_velo = read_track(gpx)
        create_polygone(route_map, track_velo, color, name) #005881') #08007A')

    return route_map


@app.route("/")
def fullscreen():
    """Simple example of a fullscreen map."""
    m = create_map()
    return m.get_root().render()


@app.route("/iframe")
def iframe():
    """Embed a map as an iframe on a page."""
    m = folium.Map()

    # set the iframe width and height
    m.get_root().width = "800px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head></head>
                <body>
                    <h1>Using an iframe</h1>
                    {{ iframe|safe }}
                </body>
            </html>
        """,
        iframe=iframe,
    )


@app.route("/components")
def components():
    """Extract map components and put those on a page."""
    m = folium.Map(
        width=800,
        height=600,
    )

    m.get_root().render()
    header = m.get_root().header.render()
    body_html = m.get_root().html.render()
    script = m.get_root().script.render()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head>
                    {{ header|safe }}
                </head>
                <body>
                    <h1>Using components</h1>
                    {{ body_html|safe }}
                    <script>
                        {{ script|safe }}
                    </script>
                </body>
            </html>
        """,
        header=header,
        body_html=body_html,
        script=script,
    )


if __name__ == "__main__":
    app.run(debug=True)