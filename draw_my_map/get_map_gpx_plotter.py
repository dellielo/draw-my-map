from gpxplotter import (
    read_gpx_file,
    create_folium_map,
    # add_segment_to_map,
    add_all_tiles,
)
import os
from draw_my_map.gpxplotter_mine import (
    add_segment_to_map
)

import folium
import streamlit as st 

def build_map(the_map, DICT_PATH_GPX) :
    group_seg = {}
    print(DICT_PATH_GPX)
    for name_group, infos_tracks in DICT_PATH_GPX.items() : 
        print(infos_tracks)
        path_folder_gpx, color = infos_tracks
        all_seg = []
        if isinstance(path_folder_gpx, list):
            list_gpx =  path_folder_gpx
        elif os.path.isdir(path_folder_gpx) :
            list_gpx = [path_folder_gpx + file for file in os.listdir(path_folder_gpx)] 
        else :
            print('Error ...')

        for ind_file, path_gpx_test in enumerate(list_gpx):
            print("ihriheriihr", path_gpx_test)
            # if ind_file > 2 :
            #     continue
            # path_gpx_test = path_folder_gpx + file
        
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

