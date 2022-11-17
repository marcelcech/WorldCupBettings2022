# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd

# -------------------------------------------- data import starts ------------------------------------------------- #
# this will only happen once after app.py starts
df = pd.read_excel("https://github.com/MCechgh/WorldCupBettings/blob/main/backend/database.xlsx?raw=true", index_col=0)

tip_cols = []
score_cols = []
name_cols = []

for col_name in df.columns:
    if 'tip' in col_name[:3]:
        tip_cols.append(col_name)
        name_cols.append(col_name[4:])
    if 'score' in col_name[:5]:
        score_cols.append(col_name)

for name, tip, score in zip(name_cols, tip_cols, score_cols):
    print('Short check', name, tip, score)

played_matches = df[df['results'].notna()]
upcoming_matches = df[df['results'].isna()]

 
# -------------------------------------------- data import ends ------------------------------------------------- #

# ------------------------------- defining plots and texts starts  ------------------------------------------------- #
def _make_fever_curve():
    fever_curve = df[score_cols].cumsum()
    fever_curve.index += 1
    fever_curve.index.name = 'Match No.'

    fig = px.line(fever_curve, x=fever_curve.index, y=fever_curve.columns, labels={
        "value": "Score",
        "variable": "Legend"
    },
                  title="Score evolution")

    last_played_match = df[df['results'].notna()].index[-1]
    fig.add_vline(x=last_played_match + 1, annotation_text="last played match", annotation_position="bottom right")

    return dcc.Graph(
        figure=fig
    )


def _make_scoreboard():
    curr_scores = df[score_cols].sum()
    curr_scores = pd.DataFrame({'Name': name_cols, 'Score': curr_scores.values,
                                'Last bets': [str(played_matches[f'tip {name}'].values[-4:]) for name in name_cols],
                                'Upcoming bets': [str(upcoming_matches[f'tip {name}'].values[:4]) for name in
                                                  name_cols]})
    curr_scores.sort_values('Score', ascending=False, inplace=True)
    curr_scores['Place'] = range(1, curr_scores.index.size + 1)

    for i in range(curr_scores.index.size - 1):
        if curr_scores.loc[i, 'Score'] == curr_scores.loc[i + 1, 'Score']:
            curr_scores.loc[i + 1, 'Place'] = curr_scores.loc[i, 'Place']

    # curr_scores.set_index('Place', inplace=True)
    curr_scores = curr_scores[['Place', 'Name', 'Score', 'Last bets', 'Upcoming bets']]

    return dash_table.DataTable(curr_scores.to_dict('records'),
                                [{"name": i, "id": i} for i in curr_scores.columns])


def _print_last_games():
    return html.Div([
        html.H3("Last matches:"),
        html.Div([
            html.Div([str(match) + ' with result ', str(result)]) for match, result in
            zip(played_matches['match'].values[-5:], played_matches['clear text results'].values[-5:])
        ])
    ], style={'textAlign': 'center'})


def _print_next_games():
    return html.Div([
        html.H3("Upcoming matches:"),
        html.Div([
            html.Div([str(match)]) for match in upcoming_matches['match'].values[:4]
        ])
    ], style={'textAlign': 'center'})


# ------------------------------- defining plots and texts starts  ------------------------------------------------- #

# ------------------------------------------------- app starts  ------------------------------------------------- #
app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(children='World cup - betting game', style={'textAlign': 'center'}),

        html.Div(children='''
                    A small dashboard for the current status of our betting game. 
                    ''', style={'textAlign': 'center'}),

        html.Br(),

        html.Div([
            html.Div(children=[
                html.Div([
                    _make_scoreboard()
                ]),
            ], style={'padding': 10, 'flex': 1}),

            html.Div(children=[
                html.Div([
                    _print_last_games()
                ]),
                html.Div([
                    _print_next_games()
                ]),

            ], style={'padding': 10, 'flex': 1}),
        ], style={'display': 'flex', 'flex-direction': 'row'}),

        html.Br(),
        html.Div([
            _make_fever_curve()
        ])
    ]

)

# ------------------------------------------------- app ends  ------------------------------------------------- #


if __name__ == '__main__':
    app.run_server(debug=True)
