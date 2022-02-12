import folium
import pandas as pd
import geopandas as gpd
import helpers
from branca.colormap import linear

desired_width = 600
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 400)

input_activities = "./raw_data/activitats/activitats2020_bars.csv"
input_neighbourhoods = "./raw_data/barris/Barris.shp"
center = [41.97969558739158, 2.8213967358161915]

act_df = gpd.read_file(input_activities)
nbh_df = gpd.read_file(input_neighbourhoods)

# Insert and Transform coordinates projection
bars_df = helpers.coordinates_to_point_activities(act_df)

# Transform geometries to a new coordinate reference system.
nbh_df = nbh_df.to_crs(epsg=4236)

# Insert random prices to bars
bars_df_with_price = helpers.add_random_price_to_df(act_df)

# Locate points inside polygon and insert into bars df
nbh_bars_dict = helpers.get_neighborhoods_location(nbh_df, bars_df_with_price)
bars_df_with_nbh = helpers.insert_neighbourhood_into_df(bars_df_with_price, nbh_bars_dict)

# Group bars into neighbourhoods
nbh_count_df = bars_df_with_nbh.groupby('NOM_COMPLE')['id'].nunique().reset_index()
nbh_count_df.rename(columns={'id':'nb'}, inplace=True)
nbh_geo_count_df = pd.merge(nbh_df, nbh_count_df, on='NOM_COMPLE')

# Calculate quote part for each neighbourhood
nbh_geo_count_df['quote_part'] = nbh_geo_count_df['nb'] / nbh_geo_count_df['nb'].sum()
nbh_geo_count_df['quote_part_pct'] = nbh_geo_count_df['quote_part'].apply(lambda x : str(round(x*100, 1)) + '%')
print(nbh_geo_count_df)

# Create a map
map_girona = folium.Map(location=center, zoom_start=13, tiles='Stamen Toner')
nbh_count_colormap = linear.YlGnBu_09.scale(min(nbh_count_df['nb']), max(nbh_count_df['nb']))
style_function = lambda x: {
    'fillColor': nbh_count_colormap(x['properties']['nb']),
    'color': 'black',
    'weight': 1.5,
    'fillOpacity': 0.7
}
folium.GeoJson(
    nbh_geo_count_df,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(
        fields=['NOM_COMPLE', 'nb', 'quote_part_pct'],
        aliases=['Neighbourhood', 'Location amount', 'Amount %'],
        localize=True
    )
).add_to(map_girona)
nbh_count_colormap.caption = 'Girona bars location amount'
nbh_count_colormap.add_to(map_girona)
map_girona.save('index.html')
