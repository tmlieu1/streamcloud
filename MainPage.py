import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go


class MainPage:
    app = dash.Dash()
    colors = {'background': '#272727',
              'text': '#ffffff'}
    data = pd.read_csv('./data/tv_shows.csv')
    data2 = data.groupby(data['Age'], as_index=False).size()
    ageGroup = data['Age'].tolist()
    dropDownDict = []
    i = 0


    def __init__(self):
        for i in range(len(self.ageGroup)):
            self.dropDownDict.append({'label': self.ageGroup[i], 'value': self.ageGroup[i]})
        # print(ageGroup)
        # print(data)
        self.app.layout = html.Div(style={'backgroundColor': self.colors['background']}, children=[
            html.H1(
                children='Hello General Kenobi',
                style={
                        'textAlign': 'center',
                        'color': self.colors['text']
                }
            ),
            html.Div(
                children='Dash: A weeb application framework for Pythoon.',
                style={
                    'textAlign': 'center',
                    'color': self.colors['text']
                }),
            dcc.Graph(
                id='Avg-age-group',
                figure={
                    'data': [{'x': self.data2['Age'], 'y': self.data2['size'], 'type': 'bar', 'name': 'Count By groups'}],
                        'layout': {
                            'plot_bgcolor': self.colors['background'],
                            'paper_bgcolor': self.colors['background'],
                            'font': {
                                'color': self.colors['text']
                            }
                        }
                    }
                ),
            dcc.Dropdown(
                id='Age-Group-Drop',
                options=self.dropDownDict,
                placeholder='Select an age group',
                clearable=False,
                searchable=False

            )
            ])

    # @app.callback(
    #     dash.dependencies.Output('Avg-age-group', 'figure'),
    #     [dash.dependencies.Input('Age-Group-Drop', 'value')])
    # def update_graph(self, age_group_drop):
    #     # df = self.data2['Age' == ageGroupDrop]
    #     fig = go.Figure(go.Bar(x=self.data2[self.data2['Age'] == age_group_drop], y=self.data2['size']))
    #     return fig

    def runPage(self):
        self.app.run_server(debug=True)

