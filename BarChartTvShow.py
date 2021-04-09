import pandas as pd
import plotly.graph_objects as go

class BarChartTvShow:
    def __init__(self, data):
        self.data = data
        self.platforms = ['Netflix', 'Prime Video', 'Hulu', 'Disney+']
        self.platColors = ['#E50914', '#00A8E1', '#1CE783', '#1038CD']

        self.figure = self.createBarChart()

    def getFigure(self):
        return self.figure

    def getPlatColors(self):
        return self.platColors

    def createBarChart(self):
        countPlatforms = []
        for platform in self.platforms:
            countPlatforms.append(self.data[platform].sum())

        fig = go.Figure(data=[
            go.Bar(x=self.platforms, y=countPlatforms, marker_color=self.platColors
                   )],
            layout={
                'paper_bgcolor': "#272D3F",
                'plot_bgcolor': "#272D3F",
                'font': {
                    'color': '#ffffff'
                }
            })
        return fig
