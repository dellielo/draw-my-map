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
from gpxplotter_mine import (
    add_segment_to_map
)
import os
from gpxplotter import (
    read_gpx_file,
    create_folium_map,
    # add_segment_to_map,
    add_all_tiles,
)

app = Flask(__name__)

PATH_COUNTRY = "G:\Mon Drive/Velo/Dive and Bike en Asie/all_shape.zip"
DICT_PATH_GPX = { "Bike" : ["G:\Mon Drive\Velo\D&B Corsica\GPX/", '#0F00FF'],
                    # "Bus" : ["G:\Mon Drive/Velo/Dive and Bike en Asie/GPX/Car/", '#FF5733'],
                    # "Train" : ["G:\Mon Drive/Velo/Dive and Bike en Asie/GPX/Train/", '#468100'],
                    # "Boat" : ["G:\Mon Drive/Velo/Dive and Bike en Asie/GPX/Boat/", '#00FFFB'],
                    }


def create_map() :
    the_map = create_folium_map(tiles='kartverket_topo4')
    # Add pre-defined tiles:
    add_all_tiles(the_map)
    
    group_seg = {}
    for name_group, infos_tracks in DICT_PATH_GPX.items() : 
        
        path_gpx, color = infos_tracks
        all_seg = []
        for ind_file, file in enumerate(os.listdir(path_gpx)):
            print("ihriheriihr", ind_file)
            if ind_file > 2 :
                continue
            path_gpx_test = path_gpx + file
        
            for track in read_gpx_file(path_gpx_test):
                print(path_gpx_test)
                for i, segment in enumerate(track['segments']):
                    # print(segment.keys())
                    segment['elevation'] = segment['elevation'] - min(segment['elevation'])
                    # all_seg = mergeDictionary(all_seg, segment) if all_seg is not None else segment
                    # all_seg = np.concatenate([all_seg, segment]]) if all_seg is not None else segment
                    # print(all_seg)
                    segment['name'] = track['name']
                    # if segment['time'][0] < start_time :
                    #     mark_start 
                    all_seg.append(segment)
        group_seg[name_group] = all_seg

    for name_group, all_seg in group_seg.items():
        group_map = folium.FeatureGroup(name= '<span style= "color:' + color +'; background-color:white ;"> '+ name_group + '</span>')
        for i, seg  in enumerate(all_seg) :           
            show_cmap = False if i>0 else True # to draw 1 cmap
            #color_by='elevation'
            add_segment_to_map(group_map, seg, show_cmap=show_cmap, color_by='elevation', cmap='viridis', min_value=0, max_value=500)
        group_map.add_to(the_map)
    # if fit_bounds:
    boundary = the_map.get_bounds()
    the_map.fit_bounds(boundary, padding=(3, 3))
    # the_map.add_child(colormap)
    # Add layer control to change tiles:
    folium.LayerControl(sortLayers=True).add_to(the_map)

    return the_map


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