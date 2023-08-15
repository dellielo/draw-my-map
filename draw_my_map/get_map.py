import folium
import geopandas as gpd
import pandas as pd
import os

# def read_one_track(filename):

def read_track(folder, filter_country=""):
    track_car = gpd.GeoDataFrame(columns=['name', 'geometry'], geometry='geometry')

    for file in os.listdir(folder):
        print(folder + file)
        if file.endswith(('.gpx')) : #and not file.startswith(filter_country):
            try:
                gdf = gpd.read_file(folder + file, layer='tracks')
                gpx = gdf[['name', 'geometry']]
                # print(folder + file, "accepted")
                # track_car = track_car.append(gpx) 
                track_car = pd.concat([track_car, gpx])
                
            except Exception as e:
                print("Error", e, file) 

    track_car.sort_values(by="name", inplace=True)
    track_car.reset_index(inplace=True, drop=True)
    track_car = track_car.explode()
    return track_car

def create_polygone(route_map, tracks, color, name):
  # print('<span style= "background-color: ' + color +';"> '+ name + '</span>')
    group = folium.FeatureGroup(name= '<span style= "color:' + color +'; background-color:white ;"> '+ name + '</span>')
    for ind, (_, row_car) in enumerate(tracks.iterrows()):
        sim_geo_car = gpd.GeoSeries(row_car['geometry']).simplify(tolerance=0.001)
        geo_j_car = sim_geo_car.to_json()
        start = row_car['geometry'].coords[0]
        end = row_car['geometry'].coords[-1]

        style1 = {'color': color, "opacity": 0.99, "weight":3} #017c81ff

        geo_fol_car = folium.GeoJson(data=geo_j_car,  control=False, 
                                style_function=lambda x: style1)
        geo_fol_car.add_child(folium.Popup(row_car["name"]))
        geo_fol_car.add_to(group)
 
        for point in [[start[1], start[0]], [end[1], end[0]]]:
            name_point = row_car['name']
        
            folium.Circle(location=[point[0], point[1]],
                        popup=name_point, 
                        color='black',
                        fill=True,
                        fill_color='black',
                        weight=2, 
                        radius=3,
                        opacity= 0.90,
                        fillOpacity= 1,
                        ).add_to(group)

    group.add_to(route_map)

def draw_shape(route_map, path_shape, list_country_show=[], exclude=False):
    df = gpd.read_file(path_shape)
    for _, r in df.iterrows():
        if exclude :
            if 'COUNTRY' in r and r['COUNTRY'] not in list_country_show :
                dict_color = {'fillColor': 'white', 'fillOpacity':0.5, 'color': 'black', 'opacity': 0.11, "weight":1}
            else: 
                continue
        else :
            dict_color = {'fill': False, 'color': 'black', 'opacity': 0.5, "weight":1}
            if 'COUNTRY' in r and r['COUNTRY'] in list_country_show :
                continue
            elif 'COUNTRY' not in r:
                a = 0
                dict_color = {'fill': False, 'color': 'black', 'opacity': 0.1, "weight":1}
            else :
                continue

        sim_geo = gpd.GeoSeries(r['geometry']) #.simplify(tolerance=0.1)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j, control=False, 
                            style_function=lambda x: dict_color)
        geo_j.add_to(route_map)
    return route_map


