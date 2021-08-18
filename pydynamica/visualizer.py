import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
import plotly.express as px
from collections import deque

from env import Env

x = deque(maxlen = 20)
x.append(1)

y = deque(maxlen=20)
y.append(0)

food = deque(maxlen=20)
minerals = deque(maxlen=20)
food.append(0)
minerals.append(0)

app = dash.Dash(__name__)
app.layout = html.Div (
    [
        html.H1(children='GDP Per Capita'),
        dcc.Graph(id='gdp-graph', animate=True),
        html.H1(children="Avg Internal Values"),
        dcc.Graph(id='food-graph', animate=True),
        dcc.Interval(
            id="graph-update",
            interval = 1000,
            n_intervals=0,
        ),
    ]
)

env = Env(num_agents=100, dim=(100,100))
data = []

@app.callback(
    [Output('gdp-graph', 'figure'), Output('food-graph', 'figure')],
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    x.append(x[-1] + 1)
    out = env.step()
    y.append(out['gdp_per_cap'])
    
    food.append(out['avg_food_value'])
    minerals.append(out['avg_mineral_value'])
    
    data = plotly.graph_objs.Scatter(
        x = list(x),
        y = list(y),
        name="GDP Per Capita",
        mode="lines+markers"
    )

    food_trace = plotly.graph_objs.Scatter(
            x = list(x),
            y = list(food),
            name="Average Food Value",
            mode="lines+markers")
    mineral_trace = plotly.graph_objs.Scatter(
            x = list(x),
            y = list(minerals),
            name="Average Mineral Value",
            mode="lines+markers")
   
    gdp_out = {'data': [data],'layout': go.Layout(xaxis=dict(range=[min(x), max(x)]), yaxis=dict(range = [min(y), max(y)]))}
    food_out = {'data': [food_trace, mineral_trace], 'layout': go.Layout(xaxis=dict(range=[min(x), max(x)]), yaxis=dict(range = [min(min(food), min(minerals)), max(max(food), max(minerals))]))}

    return gdp_out, food_out 

if __name__ == "__main__":
    app.run_server()
