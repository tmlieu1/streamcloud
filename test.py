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
# fig.show()


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

datafAllTrees = pd.DataFrame(columns=['label', 'id', 'parent', 'value', 'color'])
totalData = len(data)
sumofGen = 0
# print(len(allDfgGenres['Action'][allDfgGenres['Action']['Netflix'] == 1]))
for i, platform in enumerate(platforms):

    if i > len(platforms):
        continue
    for gen in allGenres:
        numberOfGen = len(allDfgGenres[gen][allDfgGenres[gen][platform] == 1])
        sumofGen += len(allDfgGenres[gen][allDfgGenres[gen][platform] == 1])
        totalNumOnPlat = len(data[data[platform] == 1])
        seriesRow = pd.Series(dict(label=gen, id=gen+platform, parent=platform, value=numberOfGen,
                                   color=numberOfGen/totalNumOnPlat))
        # dataFrameTree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        # dataFrameTree['id'] = gen
        # dataFrameTree['parent'] = platform
        # genreDF = allDfgGenres[gen].copy()
        # dataFrameTree['value'] = len(allDfgGenres[gen][allDfgGenres[gen][platform] == 1])
        # dataFrameTree['color'] = len(allDfgGenres[gen][allDfgGenres[gen][platform] == 1])
        datafAllTrees = datafAllTrees.append(seriesRow, ignore_index=True)

# print(datafAllTrees)
summamama = 0
    # add platform
for platform in platforms:
    numberOfPlat = len(data[data[platform] == 1])
    summamama += len(data[data[platform] == 1])
    seriesRow = pd.Series(dict(label=platform, id=platform, parent='All Movies', value=numberOfPlat,
                               color=numberOfPlat / totalData))
    # dataFrameTree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
    # dataFrameTree['id'] = platform
    # dataFrameTree['parent'] = 'All Movies'
    # dataFrameTree['value'] = len(data[data[platform] == 1])
    # dataFrameTree['color'] = len(data[data[platform] == 1])
    datafAllTrees = datafAllTrees.append(seriesRow, ignore_index=True)
total = pd.Series(dict(label='All Movies', id='All Movies', parent='', value=len(data), color=1))
datafAllTrees = datafAllTrees.append(total, ignore_index=True)

print("Sum of platforms =", summamama, "\nSum of data =", len(data), "\nSum of Gen =", sumofGen)

# print(datafAllTrees)

figure2 = go.Figure(go.Treemap(
    labels=datafAllTrees['label'],
    ids=datafAllTrees['id'],
    parents=datafAllTrees['parent'],
    values=datafAllTrees['value'],
    branchvalues='remainder',
    # sort=True,
    # level='id',
    marker_colorscale='Blues',
    # marker=dict(
    #     colors=datafAllTrees['color'],
    #     colorscale='blues',
    #     cmid=totalData/4),
    hovertemplate='<b>%{label} </b> <br> Number Of Movies: %{value}',
    maxdepth=2,
    tiling_packing="binary"
    # tiling_squarifyratio=30
))

figure2.show()


# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/sales_success.csv')
# print(df.head())
#
# levels = ['salesperson', 'county', 'region'] # levels used for the hierarchical chart
# color_columns = ['sales', 'calls']
# value_column = 'calls'
#
# def build_hierarchical_dataframe(df, levels, value_column, color_columns=None):
#     """
#     Build a hierarchy of levels for Sunburst or Treemap charts.
#
#     Levels are given starting from the bottom to the top of the hierarchy,
#     ie the last level corresponds to the root.
#     """
#     df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
#     for i, level in enumerate(levels):
#         df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
#         dfg = df.groupby(levels[i:]).sum()
#         # print("dfg", dfg)
#         dfg = dfg.reset_index()
#         # print('dfg level:', dfg[level].copy())
#         df_tree['id'] = dfg[level].copy()
#         if i < len(levels) - 1:
#             df_tree['parent'] = dfg[levels[i+1]].copy()
#         else:
#             df_tree['parent'] = 'total'
#         df_tree['value'] = dfg[value_column]
#         print("df val:", df_tree['value'])
#         df_tree['color'] = dfg[color_columns[0]] / dfg[color_columns[1]]
#         print("df color", df_tree['color'])
#         df_all_trees = df_all_trees.append(df_tree, ignore_index=True)
#     total = pd.Series(dict(id='total', parent='',
#                               value=df[value_column].sum(),
#                               color=df[color_columns[0]].sum() / df[color_columns[1]].sum()))
#     df_all_trees = df_all_trees.append(total, ignore_index=True)
#     return df_all_trees
#
# df_all_trees = build_hierarchical_dataframe(df, levels, value_column, color_columns)
# average_score = df['sales'].sum() / df['calls'].sum()
# fig = go.Figure(go.Treemap(
#     labels=df_all_trees['id'],
#     parents=df_all_trees['parent'],
#     values=df_all_trees['value'],
#     branchvalues='total',
#     marker=dict(
#         colors=df_all_trees['color'],
#         colorscale='RdBu',
#         cmid=average_score),
#     hovertemplate='<b>%{label} </b> <br> Sales: %{value}<br> Success rate: %{color:.2f}',
#     maxdepth=2))
#
# fig.show()
# print()
# data['Genres'].str.contains()
# data2 = data.groupby(data['Age'], as_index=False).size()
# print(data2)
#
# figure = go.Figure(go.Bar(x=data2['Age'], y=data2['size']))
# figure.show()
