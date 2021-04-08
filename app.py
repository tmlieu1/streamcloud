# =============================================================================#
# Imports & Inits                                                              #
# =============================================================================#
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_table as dt
import plotly.graph_objects as go
import TreeMaps as tm
import TableData as td

# Init
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server

# =============================================================================#
# Data & Assets                                                                #
# =============================================================================#

# Load Datasets
df_movies = pd.read_csv('./data/movies.csv')
df_shows = pd.read_csv('./data/tv_shows.csv')

# Generate Idioms for Movies
treemaps = tm.TreeMapGraph(df_movies)
table = td.TableData(df_movies, True, False)
cleanData = table.getCleanData()
tableSearch = td.TableData(df_movies, True, True)
cleanDataSearch = tableSearch.getCleanData()
allGenress = treemaps.getAllGenres()
allGenress.sort()

# Generate Idioms for TV Shows
tableTV = td.TableData(df_shows, False, False)
cleanDataShows = tableTV.getCleanData()
tableTVSearch = td.TableData(df_shows, False, True)
cleanDataTVSearch = tableTVSearch.getCleanData()

# Fill Dropdown filters
dropDownOptions = []
for genre in allGenress:
    dropDownOptions.append({'label': genre, 'value': genre})

# Assets
streamcloud_logo = './assets/streamcloud_logo.png'

# =============================================================================#
# Colors & Styling                                                             #
# =============================================================================#
colors = {'background': '#202530', 'navigation': '#272D3F',
          'text': '#ffffff', "lightText": "#ABD6FE", "lightblueText": "#7196bb"}

navbarStyle = {
    "position": "fixed",
    "width": "100%",
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
    'margin-bottom': '1px',
}

sidebarLinkStyle = {
    "color": colors["lightText"], 
    "font-family": "Roboto", 
    "font-size": "24px",
    "font-weight": "normal"
}

dropdownStyle = { 
	"font-family": "Roboto", 
	"font-size": "20px",
    "font-weight": "bold",
    "background-color": "#3b495f",
    "color": "#ABD6FE"
}

mainHomeStyle = {
    "position": "relative",
    "zIndex": 100,
    "left": 60,
    "margin-left": "10rem",
    "margin-right": "4rem",
    'padding': '5rem 1rem 2rem 4rem',
    "background-color": "#202530",
}

searchbarStyle = {
    "font-family": "Roboto",
    "font-size": "16px",
    "border": "1.5px #202530",
    "border-radius": "10px",
    "height": "40px",
    "width": "400px",
    "margin-bottom": "0.5rem",
    "outline": 0,
    "background-color": "#3b495f",
    "color": "#7196bb"
}

tabsStyle = {
    "font-family": "Roboto",
    "font-size": "24px",
    "font-weight": "normal",
    "text-transform": "capitalize"
}

tabStyle = {
    'width': 'inherit',
    'border': 'none',
    'paddingTop': 0,
    'paddingBottom': 0,
    'height': '40px',
    "background": "#272D3F",
    "color": colors["lightText"]
}

tabSelectedStyle = {
    'width': 'inherit',
    'boxShadow': 'none',
    'borderLeft': 'none',
    'borderRight': 'none',
    'borderTop': 'none',
    'borderBottom': '3px #ffffff solid',
    'paddingTop': 0,
    'paddingBottom': 0,
    'height': '40px',
    'background': '#272D3F',
    "color": colors["lightText"]
}

# =============================================================================#
# Div Elements                                                                 #
# =============================================================================#
def buildNavbar():
	return html.Div([
            dbc.Navbar([
                dbc.Row([
                    dbc.Col(html.Img(src='./assets/streamcloud_logo.png', 
                        height="30px"), style={"padding-right": "30px"}),
                ]),
                html.Span(
                    dcc.Tabs(id='streamcloud-tabs', value="movies", 
                        persistence=True, persistence_type="local", children=[
                        dcc.Tab(
                            label="Movies",
                            value='movies',
                            style=tabStyle,
                            selected_style=tabSelectedStyle,
                        ),
                        dcc.Tab(
                            label="TV Shows",
                            value='tvshows',
                            style=tabStyle,
                            selected_style=tabSelectedStyle
                        )
                    ],style=tabsStyle),
                    className="ml-auto"
                )],
        color='#272D3F'
        )],
        style=navbarStyle
    )

def buildSidebar():
	return html.Div([
            # Movies navigation
            dbc.Nav([
                dbc.NavLink("Home", href="/", active="exact", 
                    style=sidebarLinkStyle),
                dbc.NavLink("Analytics", href="/analytics", active="exact", 
                    style=sidebarLinkStyle),
                dbc.NavLink("Search", href="/search", active="exact",
                    style=sidebarLinkStyle)
            ],
                id="navMovies",
                vertical=True,
                pills=True,
                style={"display": "block"}
            ),
            # TV Shows navigation
            dbc.Nav([
                dbc.NavLink("Home", href="/tv", active="exact",
                    style=sidebarLinkStyle),
                dbc.NavLink("Analytics", href="/tv/analytics", active="exact",
                    style=sidebarLinkStyle),
                dbc.NavLink("Search", href="/tv/search", active="exact",
                    style=sidebarLinkStyle)
            ],
                id="navTV",
                vertical=True,
                pills=True,
                style={"display": "none"}
            ),
            # Line & Filters Text
            html.Hr(style={"border-top": "2px solid", "color": "#3B495F"}),
            html.H2("Filters", 
                style={"color": colors["lightText"], 
                    "font-family": "Roboto", 
                    "font-size": "24px",
                    "text-transform": "capitalize"}),
            # Movies Dropdown
            dcc.Dropdown(
                id="platform-filter",
                options=[
                {'label': 'Netflix', 'value': 'Netflix'},
                {'label': 'Prime Video', 'value': 'Prime Video'},
                {'label': 'Hulu', 'value': 'Hulu'},
                {'label': 'Disney+', 'value': 'Disney+'}
            ],
                placeholder= "Select a platform",
				style = dropdownStyle
            ),
            # TV Dropdown
            dcc.Dropdown(
                id="platform-filter-tv",
                options=[
                {'label': 'Netflix', 'value': 'Netflix'},
                {'label': 'Prime Video', 'value': 'Prime Video'},
                {'label': 'Hulu', 'value': 'Hulu'},
                {'label': 'Disney+', 'value': 'Disney+'}
            ],
                placeholder= "Select a platform",
				style = {"display": "none"}
            ),
			html.Span(style={"position": "relative", "padding": "1px"}),
            dcc.Dropdown(
                id="genre-filter",
                options=dropDownOptions,
                placeholder="Select a genre",
				style = dropdownStyle
            )], style = sidebarStyle
		)

def buildHome():
    return html.Div(id="main-page", style=mainHomeStyle, children=[
        # Overview Text
        html.H1(
            'Overview',
            style={
                'textAlign': 'left',
                'text-transform': 'capitalize',
                'font-family': 'Roboto',
                'color': colors['lightText'],
                'padding-bottom': '5px'
            }
        ),
        # Graph
        dcc.Graph(
            id='tree-map',
            figure=treemaps.getFigure(),
            style={
                "margin-bottom": "20px",
                "box-shadow": "2px 8px 8px 1px rgba(25, 25, 25, 0.8)"
            }
        ),
        table.getDataTable()
    ])

def buildHomeTV():
    return html.Div(id="main-page-tv", style=mainHomeStyle, children=[
        # Overview Text
        html.H1(
            'Overview',
            style={
                'textAlign': 'left',
                'text-transform': 'capitalize',
                'font-family': 'Roboto',
                'color': colors['lightText'],
                'padding-bottom': '5px'
            }
        ),
        tableTV.getDataTable()
    ])

def buildSearch():
    return html.Div(id="search-page", style=mainHomeStyle, children=[
        html.H1(
            'Search',
            style={
                'textAlign': 'left',
                'text-transform': 'capitalize',
                'font-family': 'Roboto',
                'color': colors['lightText'],
                'padding-bottom': '5px'
            }
        ),
        dbc.Input(id="search-movies", type="search", placeholder="Search...", style = searchbarStyle),
        html.Span(),
        tableSearch.getDataTable()
    ])

def buildSearchTV():
    return html.Div(id="search-page-tv", style=mainHomeStyle, children=[
        html.H1(
            'Search',
            style={
                'textAlign': 'left',
                'text-transform': 'capitalize',
                'font-family': 'Roboto',
                'color': colors['lightText'],
                'padding-bottom': '5px'
            }
        ),
        dbc.Input(id="search-tv", type="search", placeholder="Search...", style = searchbarStyle),
        html.Span(),
        tableTVSearch.getDataTable()
    ])

# =============================================================================#
# Callbacks                                                                    #
# =============================================================================#

# Update search for tv shows in search page
@app.callback(
    Output('Data-Table-TV-Search', "data"),
    Input("search-tv", "value")
)
def updateSearchTableTV(query):
    if query is None:
        return cleanDataTVSearch.to_dict('records')
    if query is not None:
        filteredData = cleanDataTVSearch[cleanDataTVSearch['Title'].str.lower().str.contains(query.lower())]
    return filteredData.to_dict('records')

# Update search for movies in search page
@app.callback(
    Output('Data-Table-Search', "data"),
    Input("search-movies", "value")
)
def updateSearchTable(query):
    if query is None:
        return cleanDataSearch.to_dict('records')
    if query is not None:
        filteredData = cleanDataSearch[cleanDataSearch['Title'].str.lower().str.contains(query.lower())]
    return filteredData.to_dict('records')

# Sidebar filtering
@app.callback(
    Output('tree-map', 'figure'),
    Input('platform-filter', 'value'),
    Input('genre-filter', 'value'),
    Input('tree-map', 'figure')
)
def updateTreeMap(platformDropdownValue, genreDropdownValue, fig):
    if fig is None:
        return dash.no_update
    tempFig = fig
    if platformDropdownValue is None and genreDropdownValue is None:
        tempFig['data'][0]['level'] = 'All Movies'
        return tempFig
    if platformDropdownValue is not None and genreDropdownValue is None:
        tempFig['data'][0]['level'] = platformDropdownValue
        return tempFig
    if genreDropdownValue is not None and platformDropdownValue is not None:
        tempFig['data'][0]['level'] = genreDropdownValue + platformDropdownValue
        return tempFig
    return dash.no_update

# Filtering table data by dropdown
@app.callback(
    Output('Data-Table', 'data'),
    [Input('platform-filter', 'value'),
     Input('genre-filter', 'value'),
     Input('tree-map', 'clickData')]
)
def filterDataByComboBox(platformDropdownValue, genreDropdownValue, data):

    # print(treemaps)
    if data is None and (platformDropdownValue is None and genreDropdownValue is None):
        return cleanData.to_dict('records')

    if platformDropdownValue is None and genreDropdownValue is None and (data['points'][0]['currentPath'] == '/' or
                                                                         data['points'][0]['parent'] == 'All Movies'):
        return cleanData.to_dict('records')

    if data is not None and data['points'][0]['currentPath'] != '/':
        # print("The data:", treeData['data'][0]['level'])
        # if data['points'][0]['currentPath'] == '/':
        #     return cleanData.to_dict('records')
        idOfData = data['points'][0]['label']
        # print("label:", idOfData)
        if data['points'][0]['parent'] == 'All Movies':
            filteredData = cleanData[cleanData['Platform'].str.contains(idOfData)]
            return filteredData.to_dict('records')
        else:
            filteredData = cleanData[cleanData['Platform'].str.contains(data['points'][0]['parent'])]
            filteredData = filteredData[filteredData['Genres'].str.contains(idOfData)]
            return filteredData.to_dict('records')

    if platformDropdownValue is not None and genreDropdownValue is None:
        filteredData = cleanData[cleanData['Platform'].str.contains(platformDropdownValue)]

    if genreDropdownValue is not None and platformDropdownValue is None:
        filteredData = cleanData[cleanData['Genres'].str.contains(genreDropdownValue)]

    if platformDropdownValue is not None and genreDropdownValue is not None:
        filteredData = cleanData[cleanData['Platform'].str.contains(platformDropdownValue)]
        filteredData = filteredData[filteredData['Genres'].str.contains(genreDropdownValue)]
    return filteredData.to_dict('records')

# Updates tv shows platform table by dropdown
@app.callback(
    Output('Data-Table-TV', 'data'),
    Input('platform-filter-TV', 'value')
)
def filterTVDataByComboBox(platformDropdownValue):
    if platformDropdownValue is None:
        return cleanDataShows.to_dict('records')
    if platformDropdownValue is not None:
        filteredData = cleanDataShows[cleanDataShows['Platform'].str.contains(platformDropdownValue)]
    return filteredData.to_dict('records')

# Updating movies platform dropdown by treemap
@app.callback(
    Output('platform-filter', 'value'),
    Input('tree-map', 'clickData'),
    State('platform-filter', 'value')
)
def updatePlatformDropDown(data, value):
    if data is None:
        return dash.no_update
    if value is None and data['points'][0]['parent'] == 'All Movies':
        return data['points'][0]['id']
    if value is not None and data['points'][0]['currentPath'] == '/':
        return None
    # if data['points'][0]['currentPath'] == '/' and value is not None:
    #     return None
    return value

# Updating movies genre dropdown by treemap
@app.callback(
    Output('genre-filter', 'value'),
    Input('tree-map', 'clickData'),
    Input('platform-filter', 'value')
)
def updateGenreDropDown(data, value):
    if data is None:
        return dash.no_update
    if value is None or data['points'][0]['parent'] == 'All Movies':
        return None
    if value is not None and data['points'][0]['parent'] != 'All Movies' and data['points'][0]['currentPath'] != '/':
        return data['points'][0]['label']
    return dash.no_update

# @app.callback(
#     Output('Data-Table', 'data'),
#     Input('tree-maps', 'clickData')
# )
# def filterDataByTreeMap(data):
#     print("The data:", data)
#     if data is None:
#         return cleanData.to_dict('records')

# Page changes
@app.callback(
    Output("main-page", "children"),
    Input("url", "pathname")
)
def displayPage(pathname):
        if pathname == "/":
            return buildHome().children
        if pathname == "/tv":
            return buildHomeTV().children
        elif pathname == "/analytics":
            return html.P([
                "⠄⠄⠄⠄⠄⠄⢀⣠⣤⣶⣶⣶⣤⣄⠄⠄⢀⣠⣤⣤⣤⣤⣀⠄⠄⠄⠄⠄⠄⠄", html.Br(),
                "⠄⠄⠄⠄⢠⣾⣿⣿⣿⣿⠿⠿⢿⣿⣿⡆⣿⣿⣿⣿⣿⣿⣿⣷⡄⠄⠄⠄⠄⠄", html.Br(),
                "⠄⠄⠄⣴⣿⣿⡟⣩⣵⣶⣾⣿⣷⣶⣮⣅⢛⣫⣭⣭⣭⣭⣭⣭⣛⣂⠄⠄⠄⠄", html.Br(),
                "⠄⠄⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣭⠛⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠄", html.Br(),
                "⣠⡄⣿⣿⣿⣿⣿⣿⣿⠿⢟⣛⣫⣭⠉⠍⠉⣛⠿⡘⣿⠿⢟⣛⡛⠉⠙⠻⢿⡄", html.Br(),
                "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣭⣍⠄⣡⣬⣭⣭⣅⣈⣀⣉⣁⠄", html.Br(),
                "⣿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣛⡻⠿⠿⢿⣿⡿⢛⣥⣾⣿⣿⣿⣿⣿⣿⣿⠿⠋⠄", html.Br(),
                "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣩⣵⣾⣿⣿⣯⣙⠟⣋⣉⣩⣍⡁⠄⠄⠄", html.Br(),
                "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣷⡄⠄⠄", html.Br(),
                "⣿⣿⣿⣿⣿⣿⡿⢟⣛⣛⣛⣛⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⡀⠄", html.Br(),
                "⣿⣿⣿⣿⣿⡟⢼⣿⣯⣭⣛⣛⣛⡻⠷⠶⢶⣬⣭⣭⣭⡭⠭⢉⡄⠶⠾⠟⠁⠄", html.Br(),
                "⣿⣿⣿⣿⣟⠻⣦⣤⣭⣭⣭⣭⣛⣛⡻⠿⠷⠶⢶⣶⠞⣼⡟⡸⣸⡸⠿⠄⠄⠄", html.Br(),
                "⣛⠿⢿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠷⡆⣾⠟⡴⣱⢏⡜⠆⠄⠄⠄", html.Br(),
                "⣭⣙⡒⠦⠭⣭⣛⣛⣛⡻⠿⠿⠟⣛⣛⣛⣛⡋⣶⡜⣟⣸⣠⡿⣸⠇⣧⡀⠄⠄", html.Br(),
                "⣿⣿⣿⣿⣷⣶⣦⣭⣭⣭⣭⣭⣭⣥⣶⣶⣶⡆⣿⣾⣿⣿⣿⣷⣿⣸⠉⣷⠄⠄"], 
            style={
                "color": 'white',
                "left": 50,
                "margin-left": "4rem",
                "margin-right": "3rem",	
                "font-family": "Roboto", 
                "font-size": "20px",
                "font-weight": "bold",
            })
        elif pathname == "/tv/analytics":
            return html.P([
                "⠄⠄⠄⠄⠄⠄⠄⣠⣴⣶⣿⣿⡿⠶⠄⠄⠄⠄⠐⠒⠒⠲⠶⢄⠄⠄⠄⠄⠄⠄", html.Br(),
                "⠄⠄⠄⠄⠄⣠⣾⡿⠟⠋⠁⠄⢀⣀⡀⠤⣦⢰⣤⣶⢶⣤⣤⣈⣆⠄⠄⠄⠄⠄", html.Br(),
                "⠄⠄⠄⠄⢰⠟⠁⠄⢀⣤⣶⣿⡿⠿⣿⣿⣊⡘⠲⣶⣷⣶⠶⠶⠶⠦⠤⡀⠄⠄", html.Br(),
                "⠄⠔⠊⠁⠁⠄⠄⢾⡿⣟⡯⣖⠯⠽⠿⠛⠛⠭⠽⠊⣲⣬⠽⠟⠛⠛⠭⢵⣂⠄", html.Br(),
                "⡎⠄⠄⠄⠄⠄⠄⠄⢙⡷⠋⣴⡆⠄⠐⠂⢸⣿⣿⡶⢱⣶⡇⠄⠐⠂⢹⣷⣶⠆", html.Br(),
                "⡇⠄⠄⠄⠄⣀⣀⡀⠄⣿⡓⠮⣅⣀⣀⣐⣈⣭⠤⢖⣮⣭⣥⣀⣤⣤⣭⡵⠂⠄", html.Br(),
                "⣤⡀⢠⣾⣿⣿⣿⣿⣷⢻⣿⣿⣶⣶⡶⢖⣢⣴⣿⣿⣟⣛⠿⠿⠟⣛⠉⠄⠄⠄", html.Br(),
                "⣿⡗⣼⣿⣿⣿⣿⡿⢋⡘⠿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠄⠄", html.Br(),
                "⣿⠱⢿⣿⣿⠿⢛⠰⣞⡛⠷⣬⣙⡛⠻⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⠿⠛⣓⡀⠄", html.Br(),
                "⢡⣾⣷⢠⣶⣿⣿⣷⣌⡛⠷⣦⣍⣛⠻⠿⢿⣶⣶⣶⣦⣤⣴⣶⡶⠾⠿⠟⠁⠄", html.Br(),
                "⣿⡟⣡⣿⣿⣿⣿⣿⣿⣿⣷⣦⣭⣙⡛⠓⠒⠶⠶⠶⠶⠶⠶⠶⠶⠿⠟⠄⠄⠄", html.Br(),
                "⠿⡐⢬⣛⡻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡶⠟⠃⠄⠄⠄⠄⠄⠄", html.Br(),
                "⣾⣿⣷⣶⣭⣝⣒⣒⠶⠬⠭⠭⠭⠭⠭⠭⠭⣐⣒⣤⣄⡀⠄⠄⠄⠄⠄⠄⠄⠄", html.Br(),
                "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠄⠄⠄⠄⠄⠄⠄"],
            style={
                "color": 'green',
                "left": 50,
                "margin-left": "4rem",
                "margin-right": "3rem",	
                "font-family": "Roboto", 
                "font-size": "20px",
                "font-weight": "bold",
            })
        elif pathname == "/search":
            return buildSearch().children
        elif pathname == "/tv/search":
            return buildSearchTV().children
        return dbc.Jumbotron([
            html.H1("404: Not found", className="text-danger"),
            html.Hr,
            html.P(f"The pathname {pathname} was not recognised..."),
		])

# Adjust filters based on tab
@app.callback(
    Output("platform-filter", "style"),
    Output("platform-filter-tv", "style"),
    Output("genre-filter", "style"),
    Output("url", "pathname"),
    Output("navMovies", "style"),
    Output("navTV", "style"),
    Input("streamcloud-tabs", "value")
)
def showHideGenres(selectedTab):
    if selectedTab == "movies":
        return [dropdownStyle, {"display": "none"}, dropdownStyle, "/", {"display": "block"}, {"display": "none"}]
    if selectedTab == "tvshows":
        return [{"display": "none"}, dropdownStyle, {'display': 'none'}, "/tv", {"display": "none"}, {"display": "block"}]
# App Layout and Execution
app.layout = html.Div(
    children=[
        dcc.Location(id="url"),
        buildNavbar(),
        buildSidebar(),
        buildHome()
    ],
)

app.config.suppress_callback_exceptions=True

if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_ui=True, dev_tools_props_check=True)
