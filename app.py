# Imports
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import TreeMaps as tm
import dash_table as dt
import plotly.graph_objects as go
import TableData as td

# Init
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server

# Data
df_movies = pd.read_csv('./data/movies.csv')
df_shows = pd.read_csv('./data/tv_shows.csv')
data2 = df_shows.groupby(df_shows['Age'], as_index=False).size()
ageGroup = df_shows['Age'].tolist()
dropDownDict = []
i = 0
treemaps = tm.TreeMapGraph(df_movies)
table = td.TableData(df_movies)

# Assets
streamcloud_logo = './assets/streamcloud_logo.png'

# Colors and Styles
colors = {'background': '#202530', 'navigation': '#272D3F',
          'text': '#ffffff', "lightText": "#ABD6FE", "lightblueText": "#7196bb"}

navbarStyle = {
    "position": "sticky",
    "zIndex": 1000,
    "background-color": "#272D3F",
    "box-shadow": "2px 8px 8px 1px rgba(25, 25, 25, 0.8)"
}

sidebarStyle = {
    "position": "fixed",
    "zIndex": 900,
    "top": 56,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#272D3F",
    'margin-bottom': '1px'
}

dropdownStyle = {
    "font-family": "Roboto",
    "font-color": "white",
    "font-size": "20px",
    "font-weight": "bold",
    "background-color": "#3b495f",
}

mainHomeStyle = {
    "position": "relative",
    "zIndex": 100,
    "left": 60,
    "margin-left": "10rem",
    "margin-right": "4rem",
    # "padding": "2rem 1rem, 0rem, 75rem",
    'padding-left': '4rem',
    'padding-top': '2rem',
    'padding-right': '1rem',
    "background-color": "#202530",
}

searchbarStyle = {
    "font-family": "Roboto",
    "font-size": "16px",
    "border": "1.5px #202530",
    "border-radius": "10px",
    "height": "40px",
    "outline": 0,
    "background-color": "#3b495f",
}

searchbar = dbc.Row([
    dbc.Col(dbc.Input(type="search", placeholder="Search...", style=searchbarStyle)),
],
    align="center",
)


# Div Elements
def buildNavbar():
    return html.Div([
        dbc.Navbar(
            [
                dbc.Row([
                    dbc.Col(html.Img(src='./assets/streamcloud_logo.png', height="30px"),
                            style={"padding-right": "30px"}),
                    dbc.NavbarToggler(id="navbar-toggler"),
                    dbc.Collapse(searchbar, id="navbar-collapse", navbar=True)
                ],
                    align="center"
                ),
            ],
            color='#272D3F'
        )],
        style=navbarStyle
    )


def buildSidebar():
    return html.Div([
        dbc.Nav([
            dbc.NavLink("Home", href="/", active="exact",
                        style={"color": colors["lightText"], "font-family": "Roboto", "font-size": "24px"}),
            dbc.NavLink("Analytics", href="/Analytics", active="exact",
                        style={"color": colors["lightText"], "font-family": "Roboto", "font-size": "24px"})
        ],
            vertical=True,
            pills=True
        ),
        html.Hr(style={"border-top": "2px solid", "color": "#3B495F"}),
        html.H2("Filters", style={"color": colors["lightText"], "font-family": "Roboto", "font-size": "24px"}),
        dcc.Dropdown(options=[
            {'label': 'Netflix', 'value': 'net'},
            {'label': 'Prime Video', 'value': 'pv'},
            {'label': 'Hulu', 'value': 'hul'},
            {'label': 'Disney+', 'value': 'dis'}
        ],
            placeholder="Select a platform",
            style=dropdownStyle
        ),
        html.Span(style={"position": "relative", "padding": "1px"}),
        dcc.Dropdown(options=[
            {'label': 'Action', 'value': 'act'},
            {'label': 'Adventure', 'value': 'adv'},
            {'label': 'Thriller', 'value': 'Thr'}
        ],
            multi=True,
            placeholder="Select a genre",
            style=dropdownStyle
        )],
        style=sidebarStyle
    )


def buildHome():
    return html.Div(id="main-page", style=mainHomeStyle, children=[
        html.H1(
            'Hello General Kenobi',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        # Overview Text
        html.Div(
            'Dash: A weeb application framework for Pythoon.',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }),
        # Graph
        dcc.Graph(
            id='Avg-age-group',
            figure=treemaps.getFigure()
            # figure={
            #     'data': [
            #         {'x': data2['Age'], 'y': data2['size'], 'type': 'bar', 'name': 'Count By groups'}],
            #     'layout': {
            #         'plot_bgcolor': colors['background'],
            #         'paper_bgcolor': colors['background'],
            #         'font': {
            #             'color': colors['text']
            #         }
            #     }
            # }
        ),
        table.getDataTable()
    ])


# Callbacks
@app.callback(
    Output("main-page", "children"),
    Input("url", "pathname")
)
def displayPage(pathname):
    if pathname == "/":
        return buildHome().children
    elif pathname == "/Analytics":
        return html.P("YOU THOUGHT THIS WAS ANALYTICS, IT WAS I CYBER DIO!!!!!!",
                      style={
                          "color": 'white',
                          "left": 50,
                          "margin-left": "4rem",
                          "margin-right": "3rem",
                          "font-family": "Roboto",
                          "font-size": "20px",
                          "font-weight": "bold", })
    return dbc.Jumbotron([
        html.H1("404: Not found", className="text-danger"),
        html.Hr,
        html.P(f"The pathname {pathname} was not recognised..."),
    ])


# App Layout and Execution
app.layout = html.Div(
    children=[
        dcc.Location(id="url"),
        buildNavbar(),
        buildSidebar(),
        buildHome()
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
