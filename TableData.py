import dash_table

class TableData:

    def __init__(self, data, movies=True):
        self.data = data
        self.headerName = data.columns.values
        if movies:
            self.cleanMovieData()

        self.dataTable = dash_table.DataTable(
            id="Data-Table",
            columns=[{"name": i, "id": i} for i in self.data.columns],
            data=self.data.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': '#3B4154',
                # 'border': '1px solid black',
                # 'padding-right': '2rem',
                'overflow': 'hidden'
                # 'position': 'fixed',
                # 'width': '100%'
            },
            style_data={
                'padding-right': '2rem',
                # 'padding-left': '2rem'
            },
            style_table={
                # 'padding-top': '3rem',
                'overflowY': 'auto',
                'maxWidth': '100%',
                'height': '40rem'
            },

            style_cell_conditional=[
                {'if': {'column_id': 'Title'},
                 'width': '30%'},
                {'if': {'column_id': 'Country'},
                 'width': '10%'},
                {'if': {'column_id': 'Genres'},
                 'width': '10%'},
                {'if': {'column_id': 'Directors'},
                 'width': '10%'},
            ],
            style_header_conditional=[
                {'if': {'column_id': 'Runtime'},
                 'padding-right': '3rem'},
                {'if': {'column_id': 'Title'},
                 'padding-left': '1rem'}
            ],
            style_cell={
                'height': 'auto',
                'whiteSpace': 'normal',
                'width-max': '120px',
                'textAlign': 'left',
                'color': '#FFFFFF',
                'border': 'none',
                'font-family': 'Roboto',
                'font-weight': 'normal',
                'maxWidth': 95
            },
            # tooltip_data=[
            #     {
            #         column: {'value': str(value), 'type': 'markdown'}
            #         for column, value in row.items()
            #
            #     } for row in self.data.to_dict('records')
            # ],
            # tooltip_duration=None,
            style_data_conditional=[
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': '#272d3f'
                },
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#2c3245'
                },
                {'if': {'column_id': 'Runtime'},
                 'padding-right': '3rem'},
                {'if': {'column_id': 'Title'},
                 'padding-left': '1rem'}
            ],
            fixed_rows={'headers': True, 'data': 0}
        )


    def getDataTable(self):
        return self.dataTable

    def getCleanData(self):
        return self.data

    def cleanMovieData(self):
        self.data = self.data.drop(['ID', 'Unnamed: 0', 'Type'], axis=1)

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



