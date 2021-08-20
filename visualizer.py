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
from pydynamica.taxed_env import TaxedEnv

window_len = 1000
PAUSE = False

""" INIT """
def init_env(l_env=None):
    global env, data
    if l_env is not None:
        env = l_env
    else:
        env = Env(num_agents=100, dim=(50,50))
    data = []

def init_data_queues():
    global x, y, food, minerals, water 
    global richest, poorest, disparity
    global death_rate, collection_rate, resource_abundance, average_age_of_agent

    x = deque(maxlen = window_len)
    y = deque(maxlen=window_len)

    x.append(1)
    y.append(0)

    food = deque(maxlen=window_len)
    minerals = deque(maxlen=window_len)
    water = deque(maxlen=window_len)

    food.append(0)
    minerals.append(0)
    water.append(0)

    richest = deque(maxlen=window_len)
    poorest = deque(maxlen=window_len)
    disparity = deque(maxlen=window_len)

    richest.append(0)
    poorest.append(0)
    disparity.append(0)

    death_rate = deque(maxlen=window_len)
    collection_rate = deque(maxlen=window_len)
    resource_abundance = deque(maxlen=window_len)
    average_age_of_agent = deque(maxlen=window_len)

    death_rate.append(0)
    collection_rate.append(0)
    resource_abundance.append(0)
    average_age_of_agent.append(0)
    

""" DASHBOARD AND APP SETUP """
app = dash.Dash(__name__)
inner_layout = [
    html.H1(children="PyDynamica"),
    html.P(children="An agent based economic simulator"),
    html.Button('Play/Pause', id="pause-btn", n_clicks=0),
    html.Button('Reset', id="reset-btn", n_clicks=0),
    html.Br(),
    html.Br(),
    html.Button('Free Market', id='free-market', n_clicks=0),
    html.Button('10% Tax', id='10-tax', n_clicks=0),
    html.Button('40% Tax', id='40-tax', n_clicks=0),
    html.Button('90% Tax', id='90-tax', n_clicks=0),


    html.H1(children='GDP Per Capita'),
    dcc.Graph(id='gdp-graph', animate=True),

    html.H1(children="Avg Internal Values"),
    dcc.Graph(id='food-graph', animate=True),

    html.H1(children="Wealth & Society"),
    dcc.Graph(id="wealth-graph", animate=True),

    html.H1(children="Metadata"),
    dcc.Graph(id='meta-graph', animate=True),
    
    html.H1(children="Resources"),
    dcc.Graph(id="food-surface", animate=True),

    dcc.Interval(
        id="graph-update",
        interval = 900,
        n_intervals=0,
    ),
]
 
# Really hacky solution to get multiple callback methods for each button
# will have to fix but whatever
for i in range(6):
    inner_layout.append(html.Div(id=f'{i}', children=''))

app.layout = html.Div ( inner_layout )

""" UI & Buttons """
@app.callback(
    Output('0', 'children'),
    [Input('pause-btn', 'n_clicks')])
def button_callback(n1):
    global PAUSE
    PAUSE = not PAUSE
    return [""]

@app.callback(
    Output('1', 'children'),
    [Input('reset-btn', 'n_clicks')])
def button_callback(n1):
    PAUSE = False
    init_data_queues()
    init_env()
    return [""]

@app.callback(
    Output('2', 'children'),
    [Input('free-market', 'n_clicks')])
def button_callback(n1):
    PAUSE = False
    init_data_queues()
    init_env()
    return [""]

@app.callback(
    Output('3', 'children'),
    [Input('10-tax', 'n_clicks')])
def button_callback(n1):
    PAUSE = False
    init_data_queues()
    init_env(l_env=TaxedEnv(taxation_rate=0.1))
    return [""]

@app.callback(
    Output('4', 'children'),
    [Input('40-tax', 'n_clicks')])
def button_callback(n1):
    PAUSE = False
    init_data_queues()
    init_env(l_env=TaxedEnv(taxation_rate=0.4))
    return [""]

@app.callback(
    Output('5', 'children'),
    [Input('90-tax', 'n_clicks')])
def button_callback(n1):
    PAUSE = False
    init_data_queues()
    init_env(l_env=TaxedEnv(taxation_rate=0.9))
    return [""]




""" SIM & DATA COLLECTION"""
def create_trace(data, title):
    return plotly.graph_objs.Scatter(
        x = list(x),
        y = list(data),
        name=title,
        mode = "lines+markers"
    )

@app.callback(
    [Output('gdp-graph', 'figure'), 
        Output('food-graph', 'figure'), 
        Output('wealth-graph', 'figure'), 
        Output("meta-graph", 'figure'), 
        Output('food-surface','figure')],
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):

    if not PAUSE:
        out = env.step()

        x.append(x[-1] + 1)
        y.append(out['gdp_per_cap'])
        
        food.append(out['avg_food_value'])
        minerals.append(out['avg_mineral_value'])
        water.append(out['avg_water_value'])
        
        richest.append(out['max_wealth'])
        poorest.append(out['min_wealth'])
        disparity.append(out['max_wealth'] / out['min_wealth'])

        death_rate.append(out['death_rate'])
        collection_rate.append(out['collection_rate'])
        resource_abundance.append(out['abundance'])
        average_age_of_agent.append(out['avg_age'])


    gdp_trace = create_trace(y, "GDP per capita")

    richest_trace = create_trace(richest, "Wealth of top 25%")
    poorest_trace = create_trace(poorest, "Wealth of bottom 25%")
    disparity_trace = create_trace(disparity, "Wealth Disparity")

    food_trace = create_trace(food, "Average food value")
    water_trace = create_trace(water, "Average water value")
    mineral_trace = create_trace(minerals, "Average mineral value")

    death_rate_trace = create_trace(death_rate, "Death rate (%)")
    collection_rate_trace = create_trace(collection_rate, "Resource extraction efficiency increase (%)")
    resource_abundance_trace = create_trace(resource_abundance, "Resource Abundance (%)")
    average_age_of_agent_trace = create_trace(average_age_of_agent, "Average age")
    
   
    x_range = dict(range=[min(x), max(x)])

    ''' Line graphs '''
    gdp_out = {
        'data': [gdp_trace],
        'layout': go.Layout(xaxis= x_range, yaxis=dict(range = [min(y), max(y) + 10]))
    }
    food_out = {
        'data': [food_trace, mineral_trace, water_trace], 
        'layout': go.Layout(xaxis= x_range, yaxis=dict(range = [min(min(food), min(minerals)), max(max(food), max(minerals)) + 1]))
    }
    wealth_out = {
        'data': [richest_trace, poorest_trace, disparity_trace],
        'layout': go.Layout(xaxis=x_range,yaxis=dict(range=[min(poorest), max([max(richest),max(disparity)])]))
    }

    meta_out = {
        'data': [death_rate_trace, collection_rate_trace, resource_abundance_trace],
        'layout': go.Layout(xaxis=x_range,yaxis=dict(range=[0 , max(resource_abundance)]))
    }

    ''' 3D surface plots '''
    food_surface_out = {'data': [go.Surface(z=env.abundance)],
        'layout':go.Layout(title="Resource Abundance", width=500, height=500)}

    return gdp_out, food_out, wealth_out, meta_out, food_surface_out

if __name__ == "__main__":
    """ SIM ENV SETUP """
    init_data_queues()
    init_env()
    app.run_server()
