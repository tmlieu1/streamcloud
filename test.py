import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

data = pd.read_csv('./data/movies.csv')
genres = []
for genreStr in data["Genres"].tolist():
    if isinstance(genreStr, str):
        genreList = genreStr.split(",")
        for genre in genreList:
            genres.append(genre)

allGenres = list(set(genres))

platforms = ['Netflix', 'Hulu', 'Prime Video', 'Disney+']
platformsCount = [len(data[data["Netflix"] == 1]), len(data[data["Hulu"] == 1]),
                  len(data[data["Prime Video"] == 1]), len(data[data["Disney+"] == 1])]
parents = ["", 'Netflix', "", 'Hulu', "", 'Prime Video', "", 'Disney+']
fig = go.Figure(go.Treemap(labels=platforms, values=platformsCount, parents=parents, marker_colorscale='Blues'))
fig.show()

# data['Genres'].str.contains()
# data2 = data.groupby(data['Age'], as_index=False).size()
# print(data2)
#
# figure = go.Figure(go.Bar(x=data2['Age'], y=data2['size']))
# figure.show()
