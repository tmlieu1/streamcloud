import dash_table

class TableData:

    def __init__(self, data, movies=True):
        self.data = data
        self.headerName = data.columns.values
        if movies:
            self.cleanMovieData()

        self.dataTable = dash_table.DataTable(
            id="Data Table",
            columns=[{"name": i, "id": i} for i in self.data.columns],
            data=self.data.to_dict('records'),
            style_cell={
                'max-width': '160px',
                'min-width': '10px',
            }
        )

    def getDataTable(self):
        return self.dataTable

    def cleanMovieData(self):
        self.data = self.data.drop(['Unnamed: 0', 'Type'], axis=1)

        self.data.loc[self.data["Netflix"] == 1, 'Netflix'] = 'Netflix '
        self.data.loc[self.data['Netflix'] == 0, 'Netflix'] = ''

        self.data.loc[self.data['Prime Video'] == 1, 'Prime Video'] = ' Prime Video '
        self.data.loc[self.data['Prime Video'] == 0, 'Prime Video'] = ''

        self.data.loc[self.data['Hulu'] == 1, 'Hulu'] = ' Hulu '
        self.data.loc[self.data['Hulu'] == 0, 'Hulu'] = ''

        self.data.loc[self.data['Disney+'] == 1, 'Disney+'] = ' Disney+'
        self.data.loc[self.data['Disney+'] == 0, 'Disney+'] = ''

        self.data["Platform"] = self.data["Netflix"] + self.data["Prime Video"] + self.data["Hulu"] + \
                                self.data["Disney+"]

        self.data = self.data.drop(['Netflix', 'Prime Video', 'Hulu', 'Disney+'], axis=1)



