# Imports
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

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

# Assets
streamcloud_logo = './assets/streamcloud_logo.png'

# Colors and Styles
colors = {'background': '#202530', 'navigation': '#272D3F',
    'text': '#ffffff', "lightText": "#ABD6FE"}

navbar_style = {
	"position": "sticky",
	"zIndex": 1000, 
	"background-color": "#272D3F",
	"box-shadow": "2px 8px 8px 1px rgba(25, 25, 25, 0.8)"
}

sidebar_style = {
	"position": "fixed",
	"zIndex": 900,
	"top": 56,
	"left": 0,
	"bottom": 0,
	"width": "16rem",
	"padding": "2rem 1rem",
	"background-color": "#272D3F",
}

dropdown_style = { 
	"font-family": "Roboto", 
	"font-size": "20px",
    "font-weight": "bold",
    "background-color": "#3b495f",
}

mainHomeStyle = {
	"position": "relative",     
	"zIndex": 100,
	"left": 60,
	"margin-left": "10rem",
	"margin-right": "3rem",
	"padding": "2rem 1rem",
	"background-color": "#202530",
}

search_bar = dbc.Row([
	dbc.Col(dbc.Input(type="search", placeholder="Search...")),
],
	align="center",
)

# Div Elements
def build_navbar():
	return html.Div([
            dbc.Navbar(
                [
					dbc.Row([
						dbc.Col(html.Img(src='./assets/streamcloud_logo.png', height="30px"),
							style={"padding-right": "30px"}),
						dbc.NavbarToggler(id="navbar-toggler"),
						dbc.Collapse(search_bar, id="navbar-collapse", navbar=True)
					],
						align="center"
					),
                ],
                color='#272D3F'
            )],
			style = navbar_style
		)

def build_sidebar():
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
				style = dropdown_style
            ),
			html.Span(style={"position": "relative", "padding": "1px"}),
            dcc.Dropdown(options=[
                {'label': 'Action', 'value': 'act'},
                {'label': 'Adventure', 'value': 'adv'},
                {'label': 'Thriller', 'value': 'Thr'}
            ],
                multi=True,
                placeholder="Select a genre",
				style = dropdown_style
            )],
			style = sidebar_style
		)

def build_home():
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
                figure={
                    'data': [
                        {'x': data2['Age'], 'y': data2['size'], 'type': 'bar', 'name': 'Count By groups'}],
                    'layout': {
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                            'color': colors['text']
                        }
                    }
                }
            )
        ])

# Callbacks
@app.callback(
	Output("page-content", "children"), 
	Input("url", "pathname")
)
def renderPage(pathname):
        if pathname == "/":
            return build_home.children
        elif pathname == "/Analytics":
            return html.P("YOU THOUGHT THIS WAS ANALYTICS, IT WAS I CYBER DIO!!!!!!", style={"color": 'white'})
        return dbc.Jumbotron([
            html.H1("404: Not found", className="text-danger"),
            html.Hr,
            html.P(f"The pathname {pathname} was not recognised..."),
		])
		
# App Layout and Execution
app.layout = html.Div(
	id="page-content",
	children=[
		build_navbar(),
		build_sidebar(),
		build_home()
	],
)


if __name__ == "__main__":
	app.run_server(debug=True)