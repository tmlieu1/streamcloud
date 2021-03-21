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
parents = ["All Movies", "All Movies", "All Movies", "All Movies"]
fig = go.Figure(go.Treemap(labels=platforms, values=platformsCount, parents=parents, marker_colorscale='Blues'))
fig.show()


# levels will be divided into platforms and genres.
levels = ['Genres', 'Platforms']

# color columns we are looking for
color_of_columns = ['IMDb', 'Rotten Tomatoes']

allDfgGenres = {}
for i, gen in enumerate(allGenres):
    data['Genres'] = data['Genres'].apply(str)
    dfg = data[data['Genres'].str.contains(gen, case=False)]
    allDfgGenres[gen] = dfg
# print(allDfgGenres)

datafAllTrees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
for i, platform in enumerate(platforms):

    if i > len(platforms):
        continue
    for gen in allGenres:
        dataFrameTree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        dataFrameTree['id'] = gen
        dataFrameTree['parent'] = platform
        genreDF = allDfgGenres[gen]
        dataFrameTree['value'] = len(genreDF[genreDF[platform] == 1])
        dataFrameTree['color'] = len(genreDF[genreDF[platform] == 1])
        datafAllTrees = datafAllTrees.append(dataFrameTree, ignore_index=True)

print(datafAllTrees)

    # add platform
for platform in platforms:
    dataFrameTree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
    dataFrameTree['id'] = platform
    dataFrameTree['parent'] = 'All Movies'
    dataFrameTree['value'] = len(data[data[platform] == 1])
    dataFrameTree['color'] = len(data[data[platform] == 1])
    datafAllTrees = datafAllTrees.append(dataFrameTree, ignore_index=True)
total = pd.Series(dict(id='All Movies', parent='', value=len(data), color=len(data)))
datafAllTrees = datafAllTrees.append(total, ignore_index=True)

print(datafAllTrees)

figure2 = go.Figure(go.Treemap(
    labels=datafAllTrees['id'],
    parents=datafAllTrees['parent'],
    values=datafAllTrees['value'],
    branchvalues='total',
    marker=dict(
        colors=datafAllTrees['color'],
        colorscale='blues',
        cmid=len(datafAllTrees)),
    hovertemplate='<b>%{label} </b> <br> Number Of Movies: %{value}',
    maxdepth=2
))

figure2.show()
# data['Genres'].str.contains()
# data2 = data.groupby(data['Age'], as_index=False).size()
# print(data2)
#
# figure = go.Figure(go.Bar(x=data2['Age'], y=data2['size']))
# figure.show()
