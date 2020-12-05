import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import requests
import json
from pandas import DataFrame as df
import pycountry
import plotly.express as px



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('CountryDeath', external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# Import and clean data 
r = requests.get('https://api.covid19api.com/summary')
packages_json = r.json()

#print(packages_json)

# json.dumps make it more readable
packages_str = json.dumps(packages_json, indent=2)

d = df(packages_json['Countries'])

d['Country'].loc[(d['Country'] == 'United States of America')] = 'United States'


input_countries = d['Country']

# to generate 3 digit country codes from https://stackoverflow.com/questions/16253060/how-to-convert-country-names-to-iso-3166-1-alpha-2-values-using-python
countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3

codes = [countries.get(country, 'Unknown code') for country in input_countries]


d['Country_Code3'] = df(codes)
d['Country_Code3'].loc[(d['Country'] == 'Bolivia')] = 'BOL'
d['Country_Code3'].loc[(d['Country'] == 'Venezuela (Bolivarian Republic)')] = 'VEN'
d['Country_Code3'].loc[(d['Country'] == 'Korea (South)')] = 'KOR'
d['Country_Code3'].loc[(d['Country'] == 'Congo (Kinshasa)')] = 'COD'
d['Country_Code3'].loc[(d['Country'] == 'Taiwan, Republic of China')] = 'COD'
d['Country_Code3'].loc[(d['Country'] == 'Syrian Arab Republic (Syria)')] = 'SYNS'

	

# -------------------------------------------------------------------------------------------

fig = px.choropleth(d, locations="Country_Code3",
                    color="NewConfirmed", # lifeExp is a column of gapminder
                    hover_name="Country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)

app.layout = html.Div(children=[
    html.H1(children='Covid Number of Cases'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])