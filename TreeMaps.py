import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math


class TreeMapGraph:

    def __init__(self, data):
        self.data = data
        self.allGenres = []
        self.platforms = ['Netflix', 'Hulu', 'Prime Video', 'Disney+']

        self.createAllGenres()
        self.datafAllTrees = self.createMovieTreemap()
        # print(self.allGenres)
        # print(self.datafAllTrees)
        self.figure = go.Figure(go.Treemap(
            labels=self.datafAllTrees['label'],
            ids=self.datafAllTrees['id'],
            parents=self.datafAllTrees['parent'],
            values=self.datafAllTrees['value'],
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
            # tiling_packing="binary"
            # tiling_squarifyratio=30
        ),
        layout={
            'paper_bgcolor': "#272D3F",
            'font': {
                'color': '#ffffff'
            }
        })
    pass

    def getAllGenres(self):
        return self.allGenres

    def createAllGenres(self) -> None:
        genres = []
        for genreStr in self.data["Genres"].tolist():
            if isinstance(genreStr, str):
                genreList = genreStr.split(",")
                for genre in genreList:
                    genres.append(genre.strip())

        self.allGenres = list(dict.fromkeys(genres))
        print()
    pass

    def getFigure(self):
        return self.figure
    pass
    # data = pd.read_csv('./data/movies.csv')
    # genres = []
    # for genreStr in data["Genres"].tolist():
    #     if isinstance(genreStr, str):
    #         genreList = genreStr.split(",")
    #         for genre in genreList:
    #             genres.append(genre)
    #
    # allGenres = list(set(genres))

    # platforms = ['Netflix', 'Hulu', 'Prime Video', 'Disney+']
    # platformsCount = [len(data[data["Netflix"] == 1]), len(data[data["Hulu"] == 1]),
    #                   len(data[data["Prime Video"] == 1]), len(data[data["Disney+"] == 1])]
    # parents = ["All Movies", "All Movies", "All Movies", "All Movies"]
    # fig = go.Figure(go.Treemap(labels=platforms, values=platformsCount, parents=parents, marker_colorscale='Blues'))
    # fig.show()

    # levels will be divided into platforms and genres.
    # levels = ['Genres', 'Platforms']

    # color columns we are looking for
    # color_of_columns = ['IMDb', 'Rotten Tomatoes']

    def createMovieTreemap(self) -> pd.DataFrame:
        allDfgGenres = {}
        for i, gen in enumerate(self.allGenres):
            self.data['Genres'] = self.data['Genres'].apply(str)
            dfg = self.data[self.data['Genres'].str.contains(gen, case=False)]
            allDfgGenres[gen] = dfg
        # print(allDfgGenres)

        datafAllTrees = pd.DataFrame(columns=['label', 'id', 'parent', 'value', 'color'])
        totalData = len(self.data)
        sumofGen = 0
        # print(len(allDfgGenres['Action'][allDfgGenres['Action']['Netflix'] == 1]))
        for i, platform in enumerate(self.platforms):

            if i > len(self.platforms):
                continue
            for gen in self.allGenres:
                numberOfGen = len(allDfgGenres[gen][allDfgGenres[gen][platform] == 1])
                sumofGen += len(allDfgGenres[gen][allDfgGenres[gen][platform] == 1])
                totalNumOnPlat = len(self.data[self.data[platform] == 1])
                seriesRow = pd.Series(dict(label=gen, id=gen + platform, parent=platform, value=numberOfGen,
                                           color=numberOfGen / totalNumOnPlat))
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
        for platform in self.platforms:
            numberOfPlat = len(self.data[self.data[platform] == 1])
            summamama += len(self.data[self.data[platform] == 1])
            seriesRow = pd.Series(dict(label=platform, id=platform, parent='All Movies', value=numberOfPlat,
                                       color=numberOfPlat / totalData))
            # dataFrameTree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
            # dataFrameTree['id'] = platform
            # dataFrameTree['parent'] = 'All Movies'
            # dataFrameTree['value'] = len(data[data[platform] == 1])
            # dataFrameTree['color'] = len(data[data[platform] == 1])
            datafAllTrees = datafAllTrees.append(seriesRow, ignore_index=True)

        total = pd.Series(dict(label='All Movies', id='All Movies', parent='', value=len(self.data), color=1))
        datafAllTrees = datafAllTrees.append(total, ignore_index=True)

        print("Sum of platforms =", summamama, "\nSum of data =", len(self.data), "\nSum of Gen =", sumofGen)
        return datafAllTrees
    pass


# print(datafAllTrees)

# figure2 = go.Figure(go.Treemap(
#     labels=datafAllTrees['label'],
#     ids=datafAllTrees['id'],
#     parents=datafAllTrees['parent'],
#     values=datafAllTrees['value'],
#     branchvalues='remainder',
#     # sort=True,
#     # level='id',
#     marker_colorscale='Blues',
#     # marker=dict(
#     #     colors=datafAllTrees['color'],
#     #     colorscale='blues',
#     #     cmid=totalData/4),
#     hovertemplate='<b>%{label} </b> <br> Number Of Movies: %{value}',
#     maxdepth=2,
#     tiling_packing="binary"
#     # tiling_squarifyratio=30
# ))
#
# figure2.show()
