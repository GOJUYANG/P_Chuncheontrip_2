import pandas as pd
import folium
from folium.map import FitBounds

url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
state_geo = f'{url}/us-states.json'
state_unemployment = f'{url}/US_Unemployment_Oct2012.csv'
state_data = pd.read_csv(state_unemployment)

m = folium.Map(location=[48, -102], zoom_start=3)

folium.Choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=state_data,
    columns=['State', 'Unemployment'],
    key_on='feature.id',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Unemployment Rate (%)'
).add_to(m)

folium.LayerControl().add_to(m)
bounds = m.fit_bounds([[52.193636, -2.221575], [52.636878, -1.139759]])
m.add_child(FitBounds(bounds, padding_top_left=None, padding_bottom_right=None, padding=None, max_zoom=None))

m.show_in_browser()