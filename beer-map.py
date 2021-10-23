# region imports
import folium
import pandas as pd
import pymongo
import geopandas as gpd
from shapely.geometry import Point, shape
from folium import plugins

# endregion


# region Setup

client = pymongo.MongoClient("mongodb+srv://admin:admin@beermap.yrkxp.mongodb.net/beer_map_db?retryWrites=true&w=majority")
db = client.beer_map_db
color = ""
center = [41.97969558739158, 2.8213967358161915]
bars = list(db.bars.find({}, {'_id': 0}))
neighborhoods = list(db.barris.find({}, {'_id': 0, 'type': 0}))


input_barris_shapes = "./raw_data/barris/Barris.shp"
nbh_sbh_df = gpd.read_file(input_barris_shapes)
# nbh_sbh_df = nbh_sbh_df[['BARRIS', 'geometry']]
# geoPath  = neighborhoods_shapes.geometry.to_json()
# poligons = folium.features.GeoJson(geoPath)
# map_girona.add_child(poligons)
# endregion

# region Helpers

def get_marker_color(price):
    price = float(price)
    if price <= 1.80:
        return "green"
    if price >= 2.20:
        return "red"
    return "beige"


def get_neighborhoods_location(nbh_df, bars):
    for i, r in nbh_df.iterrows():
        polygon = r['geometry']
        print(r['NOM_COMPLE'])
        print(polygon)
        for bar in bars:
            bar_location_point = Point(bar['coordinates']['longitude'],bar['coordinates']['latitude'])
            is_bar_in_the_nbh = bar_location_point.within(polygon)
            if(is_bar_in_the_nbh):
                print(bar['name'] + ' està al  ' + r['NOM_COMPLE'])


# endregion

get_neighborhoods_location(nbh_sbh_df, bars)

# Create a map
# bar object to df
latitutdes = []
longitudes= []
for bar in bars:
    latitutdes.append(bar['coordinates']['latitude'])
    longitudes.append(bar['coordinates']['longitude'])
df = pd.DataFrame({
    'latitude': latitutdes,
    'longitude': longitudes
})


locs_geometry = [Point(xy) for xy in zip(df.longitude,df.latitude)]
crs = {'init': 'epsg:25831'}
# Coordinate Reference Systems, "epsg:4326" is a common projection of WGS84 Latitude/Longitude
locs_gdf = gpd.GeoDataFrame(bars, crs=crs, geometry=locs_geometry)
map_girona = folium.Map(location=center, zoom_start=15, tiles='cartodbpositron')

# feature_cheap = folium.FeatureGroup(name='Cheap')
# feature_normal = folium.FeatureGroup(name='Normal')
# feature_expensive = folium.FeatureGroup(name='Expensive')

marker_cluster = plugins.MarkerCluster().add_to(map_girona)
for i, v in locs_gdf.iterrows():
    popup = """
    Name : <b>%s</b><br>
    Beer type : <b>%s</b><br>
    Price : <b>%.2f  </b><br>
    """ % (v['name'], v.canya['type'], v.canya['price'])

    if v.canya['price'] <= 1.80:
        folium.CircleMarker(location=[v.coordinates['latitude'], v.coordinates['longitude']],
                            radius=10,
                            tooltip=popup,
                            color='#4C9900',
                            fill_color='#4C9900',
                            fill=True).add_to(marker_cluster)
    elif v.canya['price'] >= 2.50:
        folium.CircleMarker(location=[v.coordinates['latitude'], v.coordinates['longitude']],
                            radius=10,
                            tooltip=popup,
                            color='#CC0000',
                            fill_color='#CC0000',
                            fill=True).add_to(marker_cluster)
    else :
        folium.CircleMarker(location=[v.coordinates['latitude'], v.coordinates['longitude']],
                            radius=10,
                            tooltip=popup,
                            color='#FF8000',
                            fill_color='#FF8000',
                            fill=True).add_to(marker_cluster)

# feature_cheap.add_to(map_girona)
# feature_normal.add_to(map_girona)
# feature_expensive.add_to(map_girona)
# folium.LayerControl(collapsed=False).add_to(map_girona)

# Display the map and save map to html file
map_girona.save('index.html')
