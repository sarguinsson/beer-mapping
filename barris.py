# region imports
import folium
import pandas as pd
import pymongo
import geopandas as gpd
from shapely.geometry import Point, shape
from folium import plugins

# endregion

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 400)


input_barris_shapes = "./raw_data/barris/Barris.shp"
nbh_sbh_df = gpd.read_file(input_barris_shapes)
print(nbh_sbh_df)
# nbh_sbh_df = nbh_sbh_df[['BARRIS', 'geometry']]
# print(nbh_sbh_df)
# nbh_sbh_df.head()




# nbh_count_df = listing_df.groupby('neighbourhood')['id'].nunique().reset_index()
# nbh_count_df.rename(columns={'id':'nb'}, inplace=True)
# nbh_geo_count_df = pd.merge(nbh_geo_df, nbh_count_df, on='neighbourhood')
# nbh_geo_count_df['QP'] = nbh_geo_count_df['nb'] / nbh_geo_count_df['nb'].sum()
# nbh_geo_count_df['QP_str'] = nbh_geo_count_df['QP'].apply(lambda x : str(round(x*100, 1)) + '%')
#
# from branca.colormap import linear
# nbh_count_colormap = linear.YlGnBu_09.scale(min(nbh_count_df['nb']),
#                                             max(nbh_count_df['nb']))
#
# nbh_locs_map = folium.Map(location=[48.856614, 2.3522219],
#                           zoom_start = 12, tiles='cartodbpositron')
#
# style_function = lambda x: {
#     'fillColor': nbh_count_colormap(x['properties']['nb']),
#     'color': 'black',
#     'weight': 1.5,
#     'fillOpacity': 0.7
# }
#
# folium.GeoJson(
#     nbh_geo_count_df,
#     style_function=style_function,
#     tooltip=folium.GeoJsonTooltip(
#         fields=['neighbourhood', 'nb', 'QP_str'],
#         aliases=['Neighbourhood', 'Location amount', 'Quote-part'],
#         localize=True
#     )
# ).add_to(nbh_locs_map)
#
# nbh_count_colormap.add_to(nbh_locs_map)
# nbh_count_colormap.caption = 'Airbnb location amount'
# nbh_count_colormap.add_to(nbh_locs_map)