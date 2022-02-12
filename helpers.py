import pandas as pd
import geopandas as gpd
import uuid
import folium
import random
from folium.plugins import HeatMap
from shapely.geometry import Point, shape

def coordinates_to_point(bars):
    latitutdes = []
    longitudes = []

    for bar in bars:
        latitutdes.append(bar['coordinates']['latitude'])
        longitudes.append(bar['coordinates']['longitude'])

    df = pd.DataFrame({
        'latitude': latitutdes,
        'longitude': longitudes
    })

    bars_points_geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
    crs = {'init': 'epsg:4236'}
    # Coordinate Reference Systems, "epsg:4326" is a common projection of WGS84 Latitude/Longitude
    bars_df_with_geometry = gpd.GeoDataFrame(bars, crs=crs, geometry=bars_points_geometry)

    return bars_df_with_geometry

def coordinates_to_point_activities(act_df):
    latitutdes = []
    longitudes = []

    for _,bar in act_df.iterrows():
        lat = bar['lat'].replace(',','.')
        lon = bar['lon'].replace(',', '.')
        latitutdes.append(float(lat))
        longitudes.append(float(lon))

    df = pd.DataFrame({
        'latitude': latitutdes,
        'longitude': longitudes
    })

    bars_points_geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
    crs = {'init': 'epsg:4236'}
    # Coordinate Reference Systems, "epsg:4326" is a common projection of WGS84 Latitude/Longitude
    bars_df_with_geometry = gpd.GeoDataFrame(act_df, crs=crs, geometry=bars_points_geometry)

    return bars_df_with_geometry

def add_random_price_to_df(bars_df):
    price_column = pd.Series([])

    for index,bar in bars_df.iterrows():
        price_column[index] = round(random.uniform(1.50, 3.00), 2)

    bars_df.insert(2, "Price", price_column)

    return bars_df

def locate_points_inside_polygon(nbh, bars, nbh_bar_dict):
    bars_in_nbh_dict_to_add = {}
    polygon = nbh['geometry']

    for _,bar in bars.iterrows():
        if (bar['geometry'].within(polygon)):
            # bars_in_nbh_dict_to_add[bar['name']] = nbh['NOM_COMPLE']
            bars_in_nbh_dict_to_add[bar['Nom_comercial']] = nbh['NOM_COMPLE']
            # bars_in_nbh_dict_to_add[bar['Nom_comercial']] = nbh['CPOSTAL']

    nbh_bar_dict.update(bars_in_nbh_dict_to_add)

def get_neighborhoods_location(nbh_df, bars):

    nbh_bar_dict = {}

    for _, nbh in nbh_df.iterrows():
        locate_points_inside_polygon(nbh,bars,nbh_bar_dict)

    return nbh_bar_dict

def get_postal_code_location(pc_df, bars):

    nbh_bar_dict = {}

    for _, pc in pc_df.iterrows():
        locate_points_inside_polygon(pc,bars,nbh_bar_dict)

    return nbh_bar_dict

def insert_neighbourhood_into_df(bars_df, nbh_bars_dict):
    neighbourhood_colum_values = []
    uids = []

    for _, bar in bars_df.iterrows():
        nbh_value = nbh_bars_dict.get(bar['Nom_comercial'])
        neighbourhood_colum_values.append(nbh_value)
        uids.append(uuid.uuid1())

    bars_df['NOM_COMPLE'] = neighbourhood_colum_values
    bars_df['id'] = uids
    return bars_df

def add_nbh_shapes_to_map(nbh_sbh_df, map, dict):
    for _, nbh in nbh_sbh_df.iterrows():

        # Without simplifying the representation of each borough,
        # the map might not be displayed
        sim_geo = gpd.GeoSeries(nbh['geometry'])
        geo_j = sim_geo.to_json()
        counter = count_values(dict, nbh['NOM_COMPLE'])
        print(nbh['NOM_COMPLE'],counter)
        popup = """
        Name : <b>%s</b><br>
        Bar quantity : <b>%s</b><br>
        """ % (nbh['BARRIS'], counter)

        # if ( counter > 100):
        #     geo_j = folium.GeoJson(data=geo_j, tooltip=popup, style_function=lambda x: {'fillColor': '#800026'})
        # elif ( 100 > counter >= 75):
        #     geo_j = folium.GeoJson(data=geo_j, tooltip=popup, style_function=lambda x: {'fillColor': '#BD0026'})
        # elif ( 75 > counter >= 50):
        #     geo_j = folium.GeoJson(data=geo_j, tooltip=popup, style_function=lambda x: {'fillColor': '#E31A1C'})
        # elif ( 50 > counter >= 25):
        #     geo_j = folium.GeoJson(data=geo_j, tooltip=popup, style_function=lambda x: {'fillColor': '#FC4E2A'})
        # elif ( 25 > counter >= 10):
        #     geo_j = folium.GeoJson(data=geo_j, tooltip=popup, style_function=lambda x: {'fillColor': '#FD8D3C'})
        # elif ( 10 > counter >= 5):
        #     geo_j = folium.GeoJson(data=geo_j, tooltip=popup, style_function=lambda x: {'fillColor': '#FEB24C'})
        # elif ( 5 > counter):
        #     geo_j = folium.GeoJson(data=geo_j, tooltip=popup, style_function=lambda x: {'fillColor': '#FED976'})

        geo_j = folium.GeoJson(data=geo_j, tooltip=popup, style_function=lambda x: {'fillColor': '#B0E0E6'})

        folium.Popup(nbh['NOM_COMPLE']).add_to(geo_j)
        geo_j.add_to(map)

def add_pc_shapes_to_map(map, pc_df, pc_bars_dict):
    for _, pc in pc_df.iterrows():
        sim_geo = gpd.GeoSeries(pc['geometry'])
        geo_j = sim_geo.to_json()
        counter = count_values(pc_bars_dict, pc['CPOSTAL'])
        print(pc['CPOSTAL'], counter)
        popup = """
        Postal Code : <b>%s</b><br>
        Bar quantity : <b>%s</b><br>
        """ % (pc['CPOSTAL'], counter)

        if (counter > 90):
            geo_j = folium.GeoJson(data=geo_j, tooltip=popup, style_function=lambda x: {'fillColor': '#800026'})
        elif (90 > counter >= 80):
            geo_j = folium.GeoJson(data=geo_j, tooltip=popup, style_function=lambda x: {'fillColor': '#BD0026'})
        elif (80 > counter >= 70):
            geo_j = folium.GeoJson(data=geo_j, tooltip=popup, style_function=lambda x: {'fillColor': '#E31A1C'})
        elif (70 > counter >= 60):
            geo_j = folium.GeoJson(data=geo_j, tooltip=popup, style_function=lambda x: {'fillColor': '#FC4E2A'})
        elif (60 > counter >= 50):
            geo_j = folium.GeoJson(data=geo_j, tooltip=popup, style_function=lambda x: {'fillColor': '#FD8D3C'})
        elif (50 > counter >= 25):
            geo_j = folium.GeoJson(data=geo_j, tooltip=popup, style_function=lambda x: {'fillColor': '#FEB24C'})
        elif (25 > counter):
            geo_j = folium.GeoJson(data=geo_j, tooltip=popup, style_function=lambda x: {'fillColor': '#FED976'})

        folium.Popup(pc['CPOSTAL']).add_to(geo_j)
        geo_j.add_to(map)

def add_clusters_to_map(map, bars_df):

    marker_cluster = folium.plugins.MarkerCluster().add_to(map)

    for _, bar in bars_df.iterrows():
        popup = """
        Name : <b>%s</b><br>
        Description : <b>%s</b><br>
        Price : <b>%s</b><br>
        """ % (bar['Nom_comercial'], bar['Descripcio'], bar['Price'])

        location = tuple([bar['geometry'].y, bar['geometry'].x])
        radius = 3

        if bar['Price'] <= 1.80 and bar['Price'] > 0.00:
            folium.CircleMarker(
                location=location,
                radius=radius,
                tooltip=popup,
                color='#4C9900',
                fill_color='#4C9900',
                fill=True).add_to(marker_cluster)
        elif bar['Price'] >= 2.50:
            folium.CircleMarker(
                location=location,
                radius=radius,
                tooltip=popup,
                color='#CC0000',
                fill_color='#CC0000',
                fill=True).add_to(marker_cluster)
        elif bar['Price'] == 0.00:
            folium.CircleMarker(
                location=location,
                radius=radius,
                tooltip=popup,
                color='#0066CC',
                fill_color='#0066CC',
                fill=True).add_to(marker_cluster)
        else:
            folium.CircleMarker(
                location=location,
                radius=radius,
                tooltip=popup,
                color='#FF8000',
                fill_color='#FF8000',
                fill=True).add_to(marker_cluster)

    folium.LayerControl(collapsed=False).add_to(map)

def add_points_to_map(map, bars_df):
    feature_na = folium.FeatureGroup(name='n/a')

    for _, bar in bars_df.iterrows():
        popup = """
        Name : <b>%s</b><br>
        Description : <b>%s</b><br>
        Price : <b>%s</b><br>
        """ % (bar['Nom_comercial'], bar['Descripcio'], bar['Price'])

        location = tuple([bar['geometry'].y, bar['geometry'].x])
        radius = 3

        folium.CircleMarker(
            location=location,
            radius=radius,
            tooltip=popup,
            color='#0066CC',
            fill_color='#0066CC',
            fill=True).add_to(feature_na)

    feature_na.add_to(map)
    folium.LayerControl(collapsed=False).add_to(map)

def add_colored_points_to_map(map, bars_df):
    feature_na = folium.FeatureGroup(name='n/a')
    feature_cheap = folium.FeatureGroup(name='Cheap')
    feature_normal = folium.FeatureGroup(name='Normal')
    feature_expensive = folium.FeatureGroup(name='Expensive')

    for _, bar in bars_df.iterrows():
        popup = """
        Name : <b>%s</b><br>
        Description : <b>%s</b><br>
        Price : <b>%s</b><br>
        """ % (bar['Nom_comercial'], bar['Descripcio'], bar['Price'])

        location = tuple([bar['geometry'].y, bar['geometry'].x])
        radius = 3

        if bar['Price'] <= 1.80 and bar['Price'] > 0.00:
            folium.CircleMarker(
                location=location,
                radius=radius,
                tooltip=popup,
                color='#4C9900',
                fill_color='#4C9900',
                fill=True).add_to(feature_cheap)
        elif bar['Price'] >= 2.50:
            folium.CircleMarker(
                location=location,
                radius=radius,
                tooltip=popup,
                color='#CC0000',
                fill_color='#CC0000',
                fill=True).add_to(feature_expensive)
        elif bar['Price'] == 0.00:
            folium.CircleMarker(
                location=location,
                radius=radius,
                tooltip=popup,
                color='#0066CC',
                fill_color='#0066CC',
                fill=True).add_to(feature_na)
        else:
            folium.CircleMarker(
                location=location,
                radius=radius,
                tooltip=popup,
                color='#FF8000',
                fill_color='#FF8000',
                fill=True).add_to(feature_normal)

    feature_na.add_to(map)
    feature_cheap.add_to(map)
    feature_normal.add_to(map)
    feature_expensive.add_to(map)
    folium.LayerControl(collapsed=False).add_to(map)

def add_bar_circlemarker_to_map(map, bars_df):
    feature_na = folium.FeatureGroup(name='n/a')
    feature_cheap = folium.FeatureGroup(name='Cheap')
    feature_normal = folium.FeatureGroup(name='Normal')
    feature_expensive = folium.FeatureGroup(name='Expensive')

    for _, bar in bars_df.iterrows():
        popup = """
        Name : <b>%s</b><br>
        Beer type : <b>%s</b><br>
        Price : <b>%.2f  </b><br>
        """ % (bar['name'], bar.canya['type'], bar.canya['price'])
        location = tuple([bar['geometry'].y, bar['geometry'].x])
        radius=8
        if bar.canya['price'] <= 1.80 and bar.canya['price'] > 0.00:
            folium.CircleMarker(
                location=location,
                radius=radius,
                tooltip=popup,
                color='#4C9900',
                fill_color='#4C9900',
                fill=True).add_to(feature_cheap)
        elif bar.canya['price'] >= 2.50:
            folium.CircleMarker(
                location=location,
                radius=radius,
                tooltip=popup,
                color='#CC0000',
                fill_color='#CC0000',
                fill=True).add_to(feature_expensive)
        elif bar.canya['price'] == 0.00:
            folium.CircleMarker(
                location=location,
                radius=radius,
                tooltip=popup,
                color='#0066CC',
                fill_color='#0066CC',
                fill=True).add_to(feature_na)
        else:
            folium.CircleMarker(
                location=location,
                radius=radius,
                tooltip=popup,
                color='#FF8000',
                fill_color='#FF8000',
                fill=True).add_to(feature_normal)

    feature_na.add_to(map)
    feature_cheap.add_to(map)
    feature_normal.add_to(map)
    feature_expensive.add_to(map)
    folium.LayerControl(collapsed=False).add_to(map)

def count_values(dict, value):
    res = 0
    for key in dict:
        if dict[key] == value:
            res = res + 1
    return res

def add_heatmap(map_girona,bars_df):
    # Create a list of coordinate pairs
    locations = list(zip(bars_df["geometry"].y, bars_df["geometry"].x))
    HeatMap(locations).add_to(map_girona)