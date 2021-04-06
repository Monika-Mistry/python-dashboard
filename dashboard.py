import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth as auth
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output


VALID_USERNAME_PASSWORD_PAIRS = [
    ['hello', 'world']
]

app = dash.Dash('auth')
auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

markdown_text = '''
### Dash and Markdown
A lot of text
'''

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')

app.layout = html.Div([
    # Markdown
    dcc.Markdown(children=markdown_text),
    # Graph created from CSV file
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['continent'] == i]['gdp per capita'],
                    y=df[df['continent'] == i]['life expectancy'],
                    text=df[df['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.8,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.continent.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    # Dropdown either multi or single with default value
    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value=['MTL', 'SF'],
        multi=True
    ),
    # Radio buttons with default value
    html.Label('Radio Items'),
    dcc.RadioItems(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL'
    ),
    # Checkboxes with default values
    html.Label('Checkboxes'),
    dcc.Checklist(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value=['MTL', 'SF']
    ),
    # Textbox with callback below updateOutputDiv
    html.Label('Text Box'),
    dcc.Input(
        id='myInput',
        value='Dash App',
        type='text'
    ),
    html.Div(id='myOutputDiv')
])

@app.callback(
    Output(component_id='myOutputDiv', component_property='children'),
    [Input(component_id='myInput', component_property='value')]
)
def updateOutputDiv(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

if __name__ == '__main__':
    app.run_server()