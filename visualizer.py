import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
import plotly.express as px
from collections import deque

from pydynamica.env import Env

window_len = 20

""" DATA QUEUE INIT """
x = deque(maxlen = window_len)
x.append(1)

y = deque(maxlen=window_len)
y.append(0)

food = deque(maxlen=window_len)
minerals = deque(maxlen=window_len)
food.append(0)
minerals.append(0)

richest = deque(maxlen=window_len)
poorest = deque(maxlen=window_len)
disparity = deque(maxlen=window_len)

richest.append(0)
poorest.append(0)
disparity.append(0)

""" DASHBOARD AND APP SETUP """
app = dash.Dash(__name__)
app.layout = html.Div (
    [
        html.H1(children='GDP Per Capita'),
        dcc.Graph(id='gdp-graph', animate=True),
        html.H1(children="Avg Internal Values"),
        dcc.Graph(id='food-graph', animate=True),
        html.H1(children="Wealth & Society"),
        dcc.Graph(id="wealth-graph", animate=True),
        html.H1(children="Resources"),
        dcc.Graph(id="food-surface", animate=True),
        dcc.Interval(
            id="graph-update",
            interval = 1000,
            n_intervals=0,
        ),
    ]
)

""" SIM ENV SETUP """
env = Env(num_agents=100, dim=(50,50))
data = []

""" SIM & DATA COLLECTION"""
def create_trace(data, title):
    return plotly.graph_objs.Scatter(
        x = list(x),
        y = list(data),
        name=title,
        mode = "lines+markers"
    )

@app.callback(
    [Output('gdp-graph', 'figure'), Output('food-graph', 'figure'), Output('wealth-graph', 'figure'), Output('food-surface','figure')],
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    out = env.step()

    x.append(x[-1] + 1)
    y.append(out['gdp_per_cap'])
    
    food.append(out['avg_food_value'])
    minerals.append(out['avg_mineral_value'])
    
    richest.append(out['max_wealth'])
    poorest.append(out['min_wealth'])
    disparity.append(out['max_wealth'] - out['min_wealth'])
    
    gdp_trace = create_trace(y, "GDP per capita")

    richest_trace = create_trace(richest, "Wealth of Richest Agent")
    poorest_trace = create_trace(poorest, "Wealth of Poorest Agent")
    disparity_trace = create_trace(disparity, "Wealth Disparity")

    food_trace = create_trace(food, "Average food value")
    mineral_trace = create_trace(minerals, "Average mineral value")
   
    x_range = dict(range=[min(x), max(x)])

    ''' Line graphs '''
    gdp_out = {'data': [gdp_trace],
            'layout': go.Layout(xaxis= x_range, 
                yaxis=dict(range = [min(y), max(y)]))}
    food_out = {'data': [food_trace, mineral_trace], 
            'layout': go.Layout(xaxis= x_range, 
                yaxis=dict(range = [min(min(food), min(minerals)), max(max(food), max(minerals))]))}
    wealth_out = {'data': [richest_trace, poorest_trace, disparity_trace],
             'layout': go.Layout(xaxis=x_range,
                yaxis=dict(range=[min(poorest), max(richest)]))}

    ''' 3D surface plots '''
    food_surface_out = {'data': [go.Surface(z=env.abundance)],
        'layout':go.Layout(title="Resource Abundance", width=500, height=500)}

    return gdp_out, food_out, wealth_out, food_surface_out

if __name__ == "__main__":
    app.run_server()
