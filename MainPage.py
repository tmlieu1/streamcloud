import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objects as go

# rem means relative font size.
class MainPage:

    colors = {'background': '#202530',
              'text': '#ffffff'}
    data = pd.read_csv('./data/tv_shows.csv')
    data2 = data.groupby(data['Age'], as_index=False).size()
    ageGroup = data['Age'].tolist()
    dropDownDict = []
    i = 0

    sidebar_style = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#272D3F",
    }

    mainHomeStyle = {
        "backgroundColor": colors['background'],
        "margin-left": "10rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    }

    def __init__(self):
        for i in range(len(self.ageGroup)):
            self.dropDownDict.append({'label': self.ageGroup[i], 'value': self.ageGroup[i]})
        # print(ageGroup)
        # print(data)

        self.sidebar = html.Div([
            dbc.Nav([
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Analytics", href="/Analytics", active="exact")
            ],
                vertical=True,
                pills=True
            )],
            style=self.sidebar_style
        )

        self.mainHome = html.Div(id="main-page", style=self.mainHomeStyle, children=[
            html.H1(
                'Hello General Kenobi',
                style={
                    'textAlign': 'center',
                    'color': self.colors['text']
                }
            ),
            html.Div(
                'Dash: A weeb application framework for Pythoon.',
                style={
                    'textAlign': 'center',
                    'color': self.colors['text']
                }),
            dcc.Graph(
                id='Avg-age-group',
                figure={
                    'data': [
                        {'x': self.data2['Age'], 'y': self.data2['size'], 'type': 'bar', 'name': 'Count By groups'}],
                    'layout': {
                        'plot_bgcolor': self.colors['background'],
                        'paper_bgcolor': self.colors['background'],
                        'font': {
                            'color': self.colors['text']
                        }
                    }
                }
            )
            # dcc.Dropdown(
            #     id='Age-Group-Drop',
            #     options=self.dropDownDict,
            #     placeholder='Select an age group',
            #     clearable=False,
            #     searchable=False
            #
            # )
        ])
        self.app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.app.callback(Output("main-page", "children"), [Input("url", "pathname")])(self.renderPage)
        self.app.layout = html.Div([dcc.Location(id="url"), self.sidebar, self.mainHome])


    # @app.callback(
    #     dash.dependencies.Output('Avg-age-group', 'figure'),
    #     [dash.dependencies.Input('Age-Group-Drop', 'value')])
    # def update_graph(self, age_group_drop):
    #     # df = self.data2['Age' == ageGroupDrop]
    #     fig = go.Figure(go.Bar(x=self.data2[self.data2['Age'] == age_group_drop], y=self.data2['size']))
    #     return fig

    def runPage(self):
        self.app.run_server(debug=True)


    def renderPage(self, pathname):
        if pathname == "/":
            return self.mainHome
        elif pathname == "/Analytics":
            return html.P("YOU THOUGHT THIS WAS ANALYTICS, IT WAS I CYBER DIO!!!!!!", style={"color": 'white'})
        return dbc.Jumbotron([
            html.H1("404: Not found", className="text-danger"),
            html.Hr,
            html.P(f"The pathname {pathname} was not recognised..."),
        ])
