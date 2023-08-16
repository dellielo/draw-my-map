import streamlit as st
from streamlit_folium import st_folium

from draw_my_map.get_map_gpx_plotter import (
    build_map
)
from gpxplotter import (
    read_gpx_file,
    create_folium_map,
    # add_segment_to_map,
    add_all_tiles,
)

import os
import pathlib

DICT_PATH_GPX = { "Bike" : ["G:\Mon Drive\Velo\D&B Corsica\GPX/", '#0F00FF'],
                    # "Bus" : ["G:\Mon Drive/Velo/Dive and Bike en Asie/GPX/Car/", '#FF5733'],
                    # "Train" : ["G:\Mon Drive/Velo/Dive and Bike en Asie/GPX/Train/", '#468100'],
                    # "Boat" : ["G:\Mon Drive/Velo/Dive and Bike en Asie/GPX/Boat/", '#00FFFB'],
                    }


# the_map = None


### Afficher/ cacher des pays


# uploaded_files = st.file_uploader("Choose a GPX file", accept_multiple_files=True, type=['gpx', 'GPX'])
dict_file = {}
dict_file['Bike'] = []
list_files = []

# for uploaded_file in uploaded_files:
#     if uploaded_file is not None:
#         bytes_data = uploaded_file.getvalue()
#         # data = uploaded_file.getvalue().decode('utf-8')
#         # st.write("filename:", uploaded_file.name)
#         # .splitlines()         
#         # st.session_state["preview"] = ''
#         # for i in range(0, min(5, len(data))):
#         #     st.session_state["preview"] += data[i]
#     # preview = st.text_area("CSV Preview", "", height=150, key="preview")
#     # upload_state = st.text_area("Upload State", "", key="upload_state")

def upload():
    for uploaded_file in uploaded_files:
        if uploaded_file is None:
            st.session_state["upload_state"] = "Upload a file first!"
        else:
            data = uploaded_file.getvalue() #.decode('utf-8')
            parent_path = pathlib.Path(__file__).parent.parent.resolve()           
            save_path = os.path.join(parent_path, "data")
            os.makedirs(save_path, exist_ok=True)
            complete_name = os.path.join(save_path, uploaded_file.name)
            with open(complete_name, "wb") as destination_file:
                destination_file.write(data)
            # destination_file.close()
            list_files.append(complete_name)
            # dict_file['Bike'].append((destination_file, None))
    st.session_state["upload_state"] = list_files
# st.button("Upload files to Sandbox", on_click=upload)

uploaded_files = st.file_uploader("Choose a GPX file :", accept_multiple_files=True, 
                                  on_change=upload())


# for uploaded_file in uploaded_files:
#     st.write("filename:", uploaded_file.name)
#     dict_file['Bike'].append((uploaded_file, None))

if  st.button('Create the map'):
    # upload()
    the_map = create_folium_map(tiles='opentopomap') #tiles='kartverket_topo4')
    # Add pre-defined tiles:
    add_all_tiles(the_map)
    dict_file['Bike'] = [st.session_state["upload_state"], "#54545454"]
    build_map(the_map, dict_file) #DICT_PATH_GPX)
    st.session_state['map'] = the_map

if 'map'in st.session_state and st.session_state['map'] :
    st_data = st_folium(st.session_state['map'], width=500)

# the_map.add_child(colormap)
# Add layer control to change tiles:
# folium.LayerControl(sortLayers=True).add_to(the_map)



### Charger un dossier / nom groupe ? 
# option couleur / elevation
# ajouter des marquers
