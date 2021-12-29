# region imports
import folium
import geopandas as gpd
import pandas as pd
import pymongo
from pyproj import Transformer
from shapely.geometry import Point
import fiona
from fiona.crs import from_epsg
# endregion

desired_width = 800
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_colwidth', 500)

center = [41.97969558739158, 2.8213967358161915]

# Spatial reference system
transformer = Transformer.from_crs(4326,25831)

input_bars  = "./raw_data/bars.geojson"
# input_neighbourhood_shapes = "./raw_data/barris/Barris.shp"
input_neighbourhood_shapes = "./raw_data/barris.geojson"
nbh_sbh_df  = gpd.read_file(input_neighbourhood_shapes)
nbh_sbh_df = nbh_sbh_df.to_crs(epsg=4236)
# nbh_sbh_df.to_file('./raw_data/barris.geojson', driver='GeoJSON')
bars_geo_df = gpd.read_file(input_bars, driver='GeoJSON')

print(nbh_sbh_df)

map_girona = folium.Map(location=center, zoom_start=13, tiles='cartodbpositron')

for _, r in nbh_sbh_df.iterrows():
    # Without simplifying the representation of each borough,
    # the map might not be displayed
    sim_geo = gpd.GeoSeries(r['geometry'])
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j,style_function=lambda x: {'fillColor': 'red'})
    folium.Popup(r['BARRIS']).add_to(geo_j)
    geo_j.add_to(map_girona)

map_girona.save('index.html')

# for index, row in bars_geo_df.iterrows():
#     pt = row['geometry']
#     is_bar_in_the_nbh = nbh_sbh_df.iloc[[0]]['geometry'].contains(pt)
#     print(row['name'] + ": {}".format(is_bar_in_the_nbh))
