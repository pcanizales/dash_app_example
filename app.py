
# coding: utf-8

# In[13]:

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()
df = pd.read_csv('https://raw.githubusercontent.com/pcanizales/dash_app_example/master/nama_10_gdp_1_Data.csv')
available_indicators = df['NA_ITEM'].unique()
available_countries = df['GEO'].unique()

app.layout = html.Div([
    html.H1(children='CC Final Project: Paulina Canizales Dashboard'),
    html.Div([
        html.H2(children='Graph 1: Scatter Plot'),
        html.Div([
            html.H4(children='Select indicator 1'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.H4(children='Select indicator 2'),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Final consumption expenditure'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),
    
    html.Div([
        html.H2(children='Graph 2: Line Chart'),
        html.Div([
            html.H4(children='Select Country'),
            dcc.Dropdown( id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Belgium'
            )
        ],
        style={'width': '30%', 'marginTop': 40, 'display': 'inline-block'}),
        
         html.Div([
            html.H4(children='Select Indicator'),
            dcc.Dropdown( 
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value= 'Gross domestic product at market prices'
                
            )
        ],style={'width': '30%', 'marginTop': 40, 'float': 'right', 'display': 'inline-block'})
     ]),
       dcc.Graph(id='grph2'),
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('grph2', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name):
    dff = df[df['UNIT'] == 'Current prices, million euro']
    dfff = dff[dff['GEO'] == xaxis_column_name] 
    return {
        'data': [go.Scatter(
            x=dfff['TIME'].unique(),
            y=dfff[dfff['NA_ITEM'] == yaxis_column_name]['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Year',
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 110, 'b': 50, 't': 20, 'r': 50},
            hovermode='closest'
        )
    }
   
if __name__ == '__main__':
    app.run_server()

