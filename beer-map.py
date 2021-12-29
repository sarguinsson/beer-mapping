# region imports
import folium
import pandas as pd
import pymongo
import geopandas as gpd
from shapely.geometry import Point, shape
from pyproj import Proj, Transformer
import helpers
# from helpers import locate_points_inside_polygon, get_neighborhoods_location, coordinates_to_point

from folium import plugins

# endregion

# region Setup

desired_width = 600
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 400)

client = pymongo.MongoClient("mongodb+srv://admin:admin@beermap.yrkxp.mongodb.net/beer_map_db?retryWrites=true&w=majority")
db = client.beer_map_db
input_nbh_shp = "./raw_data/barris/Barris.shp"
nbh_sbh_df = gpd.read_file(input_nbh_shp)
nbh_sbh_df = nbh_sbh_df.to_crs(epsg=4236)
color = ""
center = [41.97969558739158, 2.8213967358161915]
bars = list(db.bars.find({}, {'_id': 0}))
transformer = Transformer.from_crs("epsg:4326", "epsg:25831")

# endregion

bars_df = helpers.coordinates_to_point(bars)
nbh_bars_dict = helpers.get_neighborhoods_location(nbh_sbh_df, bars_df)

# Create a map
map_girona = folium.Map(location=center, zoom_start=13, tiles='cartodbpositron')

# helpers.add_bar_circlemarker_to_map(map_girona,bars_df) #Show bars with circlemarkers
helpers.add_nbh_shapes_to_map(nbh_sbh_df, map_girona, nbh_bars_dict) #Show neighbourhoods shapes

# Display the map and save map to html file
map_girona.save('index.html')
