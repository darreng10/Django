from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
import requests
from pandas import DataFrame as df
import pandas as pd
import json
# Create your views here.

def home(request):

    r = requests.get('https://api.covid19api.com/summary')

    packages_json = r.json()

        # json.dumps make it more readable
    packages_str = json.dumps(packages_json, indent=2)

    d = df(packages_json['Countries'])
    d['Death_Rate'] = (d['TotalDeaths']/d['TotalConfirmed'])*100
    df2 = pd.DataFrame(d, columns=['Country', 'Death_Rate', 'TotalConfirmed', 'TotalDeaths','NewConfirmed',
        'NewRecovered'])
    
    
    cases_monitor = {
        'country' : "Global", 
        'new_confirmed' : f"{packages_json['Global']['NewConfirmed']: ,d}",
        'total_confirmed' : f"{packages_json['Global']['TotalConfirmed']: ,d}",
        'total_recovered' : f"{packages_json['Global']['NewRecovered']: ,d}",

    }
    

    def bubble():
        r = requests.get('https://api.covid19api.com/summary')

        packages_json = r.json()

        # json.dumps make it more readable
        packages_str = json.dumps(packages_json, indent=2)

        d = df(packages_json['Countries'])
        d['Death_Rate'] = (d['TotalDeaths']/d['TotalConfirmed'])*100
        df1 = pd.DataFrame(d, columns=['Country', 'Death_Rate', 'TotalConfirmed', 'TotalDeaths'])

        
        fig = go.Figure(data=[go.Scatter(
        x=df1['TotalConfirmed'], y=df1['Death_Rate'],
        text=df1['Country'],
        mode='markers',
        )])
        fig.update_layout(
        	title = "Countries Covid Death Rate vs Number of Cases",
        	xaxis_title="Number of Cases",
        	yaxis_title="Death Rate"
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div



    context = {'cases_monitor' : cases_monitor, 'plot1': bubble()}
    return render(request, 'figures/home.html', context)
