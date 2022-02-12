import folium
import pandas as pd
import geopandas as gpd
import helpers

# desired_width = 600
# pd.set_option('display.width', desired_width)
# pd.set_option('display.max_columns', 30)
# pd.set_option('display.max_rows', 400)

input_activities = "./raw_data/activitats/activitats2020_bars.csv"
center = [41.97969558739158, 2.8213967358161915]

act_df = gpd.read_file(input_activities)

# Insert and Transform coordinates projection
bars_df = helpers.coordinates_to_point_activities(act_df)

# Insert random prices to bars
bars_df_with_price = helpers.add_random_price_to_df(act_df)

# Create a map
map_girona = folium.Map(location=center, zoom_start=13, tiles='Stamen Toner')

# Insert points to map
# helpers.add_points_to_map(map_girona, bars_df_with_price)
# helpers.add_colored_points_to_map(map_girona, bars_df_with_price)
helpers.add_clusters_to_map(map_girona, bars_df_with_price)


map_girona.save('index.html')
