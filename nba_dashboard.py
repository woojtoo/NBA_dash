from dash import Dash, dcc, html, Input, Output, State, ctx, MATCH, ALL
from dash._callback_context import callback_context
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd

################################
############# DATA #############
################################
season = pd.read_csv('data/season_2022.csv')
teams = pd.read_csv('data/teams.csv')
teams_geo = pd.read_html('https://en.wikipedia.org/wiki/National_Basketball_Association#Teams')[3]
teams_geo = teams_geo.iloc[:, [0, 1, 5]]
teams_geo = teams_geo.drop(15)
teams_geo['lat'] = teams_geo.iloc[:, -1].apply(lambda x: x.split(' / ')[-1].split(' ')[0][:-2])
teams_geo['lng'] = teams_geo.iloc[:, -2].apply(lambda x: x.split(' / ')[-1].split(' ')[1][:-2])
teams_geo.columns = teams_geo.columns.droplevel(1)
teams = pd.merge(teams, teams_geo, left_on='full_name', right_on='Team')
teams = teams.drop(columns=['Coordinates', 'Team'])

################################
############ LAYOUT ############
################################
# DARKLY, LUX, SLATE, QUARTZ
template = 'DARKLY'
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
load_figure_template(template)

teams_layout = html.Div([
    dbc.Row([
        dbc.Col(
            dbc.DropdownMenu([
                dbc.DropdownMenuItem(team["full_name"], id={'id': 'dropdown_team1_item', 'value': team["abbreviation"]}) for _, team in teams.iterrows()
            ], label='Denver Nuggets', id='dropdown_team1'),
            width={"size": 1, "order": 0, "offset": 0},
        ),
        dbc.Col(
            dbc.DropdownMenu([
                dbc.DropdownMenuItem(team["full_name"], id={'id': 'dropdown_team2_item', 'value': team["abbreviation"]}) for _, team in teams.iterrows()
            ], label='Los Angeles Lakers', id='dropdown_team2'),
            width={"size": 1, "order": 1, "offset": 0},
        ),
    ], justify="center"),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(
                            id='graph_PTSs'
                        ),
                        width=6
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id='graph_ASTs'
                        ),
                        width=6
                    )
                ]),
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(
                            id='graph_REBs'
                        ),
                        width=6
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id='graph_STLs'
                        ),
                        width=6
                    )
                ])
            ]),
            width=6
        )
    ]),
])


@app.callback(
    Output('dropdown_team1', 'label'),
    Input({'id': 'dropdown_team1_item', 'value': ALL}, 'n_clicks')
)
def update_dropdown_team1(drop_item):
    team = ctx.triggered_id if ctx.triggered_id else {'value': 'DEN'}
    return team['value']


@app.callback(
    Output('dropdown_team2', 'label'),
    Input({'id': 'dropdown_team2_item', 'value': ALL}, 'n_clicks')
)
def update_dropdown_team2(drop_item):
    team = ctx.triggered_id if ctx.triggered_id else {'value': 'LAL'}
    return team['value']


@app.callback(
    Output('graph_PTSs', 'figure'),
    Input('dropdown_team1', 'label'),
    Input('dropdown_team2', 'label')
)
def update_chart(team1, team2):
    df1 = (
        season[['TEAM_ABBREVIATION', 'GAME_DATE', 'PTS']]
        .query(f'TEAM_ABBREVIATION == "{team1}"')
        .set_index(['TEAM_ABBREVIATION', 'GAME_DATE'])
        .rolling(10, min_periods=1).mean()
        .reset_index()
    )
    df2 = (
        season[['TEAM_ABBREVIATION', 'GAME_DATE', 'PTS']]
        .query(f'TEAM_ABBREVIATION == "{team2}"')
        .set_index(['TEAM_ABBREVIATION', 'GAME_DATE'])
        .rolling(10, min_periods=1).mean()
        .reset_index()
    )
    df = pd.concat([df1, df2]).drop_duplicates()
    fig = px.line(df, 'GAME_DATE', 'PTS', color='TEAM_ABBREVIATION', range_y=[80, 160], template=template)
    fig.update_layout({"margin": {"l": 0, "r": 0, "b": 0, "t": 20}, "autosize": True})
    return fig

################################
# tabs
tab_league = [
    dbc.Row([
        dbc.Col(
            dbc.Button(
                "choose team",
                id="league_Popover_choose_team_button",
                color="primary",
            ),
        ),
    ],
        justify="center",
    ),
    dbc.Row([
        dbc.Col(
            dbc.Popover([
                dbc.Row([
                    dbc.Col([
                        html.H4(division, style={'text-align': 'center'}),
                        dbc.ListGroup([
                            dbc.ListGroupItem(
                                dbc.Row([
                                    dbc.Col(
                                        dbc.CardImg(
                                            src=f'https://cdn.nba.com/logos/nba/{team["id"]}/global/D/logo.svg',
                                            style={'width': 50, 'height': 50}#, 'vertical-align': 'middle'}
                                        ), width=3
                                    ),
                                    dbc.Col(
                                        dbc.CardBody(
                                            team["full_name"],
                                            style={'width': 150, 'height': 50, 'vertical-align': 'sub'}
                                        ),
                                    )
                                ], align="center"),
                                id={'id': 'league_ListGroupItem_choose_team', 'value': team['abbreviation']}
                            ) for _, team in teams.iterrows() if team['Division'] == division
                        ])
                    ]) for division in teams['Division'].unique()
                ])
            ],
                id='league_Popover_choose_team',
                is_open=True,
                target="league_Popover_choose_team_button",
                trigger="legacy",
                hide_arrow=True,
                style={'width': 1600, 'vertical-align': 'middle'}
            ),
        )
    ], justify="center"),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(
                            id='graph_PTS',
                            figure={'layout': {'height': 200}}
                        ),
                        width=6
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id='graph_AST',
                            figure={'layout': {'height': 200}}
                        ),
                        width=6
                    )
                ],
                    className="h-50"
                ),
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(
                            id='graph_REB',
                            figure={'layout': {'height': 200}}
                        ),
                        width=6
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id='graph_STL',
                            figure={'layout': {'height': 200}}
                        ),
                        width=6
                    )
                ],)
            ]),
            width=6
        )
    ]),
]


@app.callback(
    Output('graph_PTS', 'figure'),
    Output('graph_AST', 'figure'),
    Output('graph_REB', 'figure'),
    Output('graph_STL', 'figure'),
    Input({'id': 'league_ListGroupItem_choose_team', 'value': ALL}, 'n_clicks')
)
def update_chart(*args):
    team = ctx.triggered_id if ctx.triggered_id else {'value': 'LAL'}

    def rolling_avg_fig(stat, periods=10):
        df = (
            season[['TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_DATE', stat]]
            .rename(columns={'TEAM_NAME': 'TEAM', 'GAME_DATE': 'DATE'})
            .query(f'TEAM_ABBREVIATION == "{team["value"]}"')
            .set_index(['TEAM', 'DATE'])
            .drop(columns='TEAM_ABBREVIATION')
            .rolling(10, min_periods=1).mean()
            .reset_index()
        )
        df2 = df.copy()
        df2['TEAM'] = 'League average'
        df2[stat] = season[stat].mean()
        df = pd.concat([df2, df], ignore_index=True)

        fig = px.line(df, 'DATE', stat, color='TEAM',
                          range_y=[min(season[stat]), max(season[stat])], template=template)
        fig.update_layout({'margin': {'l': 20, 'r': 20, 'b': 20, 't': 20}, 'autosize': True, 'showlegend': False})
        return fig

    return (rolling_avg_fig('PTS'),
            rolling_avg_fig('AST'),
            rolling_avg_fig('REB'),
            rolling_avg_fig('STL'))

@app.callback(
    Output('league_Popover_choose_team', 'is_open'),
    Input({'id': 'league_ListGroupItem_choose_team', 'value': ALL}, 'n_clicks'),
    State('league_Popover_choose_team', 'is_open'),
)
def toggle_league_Popover_choose_team(n, is_open):
    if n:
        return not is_open
    return is_open





tab_payers = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab_league, label="league"),
        dbc.Tab(teams_layout, label="teams"),
        dbc.Tab(tab_payers, label="players"),
    ]
)

app.layout = html.Div(
    [
        tabs
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
