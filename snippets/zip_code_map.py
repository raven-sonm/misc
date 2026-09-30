# Source - https://stackoverflow.com/a/73045644
# Posted by r-beginners
# Retrieved 2026-08-19, License - CC BY-SA 4.0

from urllib.request import urlopen
import json
import requests

# Nevada Zip code
url = 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/nv_nevada_zip_codes_geo.min.json'
with urlopen(url) as response:
    nv_zip_json = json.load(response)

zip_code = []
for i in range(len(nv_zip_json['features'])):
    code = nv_zip_json['features'][i]['properties']['ZCTA5CE10']
    zip_code.append(code)

import pandas as pd
import numpy as np
df = pd.DataFrame({'zip_code': zip_code, 'value': np.random.randint(0,30, len(nv_zip_json['features']))})
df['zip_code'] = df['zip_code'].astype(str)

import plotly.express as px

fig = px.choropleth(df,
                    geojson= nv_zip_json,
                    locations='zip_code',
                    featureidkey="properties.ZCTA5CE10",
                    color='value',
                    color_continuous_scale="blues",
                    projection="mercator",
                    )

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig.show()
