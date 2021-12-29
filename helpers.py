import pandas as pd
import geopandas as gpd
import folium

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

def locate_points_inside_polygon(nbh, bars, nbh_bar_dict):
    bars_in_nbh_dict_to_add = {}
    polygon = nbh['geometry']

    for _,bar in bars.iterrows():
        if (bar['geometry'].within(polygon)):
            bars_in_nbh_dict_to_add[bar['name']] = nbh['NOM_COMPLE']

    nbh_bar_dict.update(bars_in_nbh_dict_to_add)

def get_neighborhoods_location(nbh_df, bars):

    nbh_bar_dict = {}

    for _, nbh in nbh_df.iterrows():
        locate_points_inside_polygon(nbh,bars,nbh_bar_dict)

    return nbh_bar_dict

def add_nbh_shapes_to_map(nbh_sbh_df, map, dict):
    for _, nbh in nbh_sbh_df.iterrows():
        # Without simplifying the representation of each borough,
        # the map might not be displayed
        sim_geo = gpd.GeoSeries(nbh['geometry'])
        geo_j = sim_geo.to_json()
        counter = count_values(dict, nbh['NOM_COMPLE'])
        print(nbh['NOM_COMPLE'],counter)
        if ( counter > 0):
            geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'red'})
        else:
            geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'blue'})
        folium.Popup(nbh['NOM_COMPLE']).add_to(geo_j)
        geo_j.add_to(map)

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

        if bar.canya['price'] <= 1.80 and bar.canya['price'] > 0.00:
            folium.CircleMarker(
                location=location,
                radius=10,
                tooltip=popup,
                color='#4C9900',
                fill_color='#4C9900',
                fill=True).add_to(feature_cheap)
        elif bar.canya['price'] >= 2.50:
            folium.CircleMarker(
                location=location,
                radius=10,
                tooltip=popup,
                color='#CC0000',
                fill_color='#CC0000',
                fill=True).add_to(feature_expensive)
        elif bar.canya['price'] == 0.00:
            folium.CircleMarker(
                location=location,
                radius=10,
                tooltip=popup,
                color='#0066CC',
                fill_color='#0066CC',
                fill=True).add_to(feature_na)
        else:
            folium.CircleMarker(
                location=location,
                radius=10,
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