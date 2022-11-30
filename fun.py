import copy

import matplotlib.pyplot as plt
import numpy as np
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# -------------------------------------------- implement traj. ---------------------------------------------------- #
def simulate_add_points():
    a = np.random.randint(0, 16)

    if a < 8:
        return 1

    if a < 12:
        return 2

    if a < 14:
        return 3

    if a < 15:
        return 4

    else:
        return 5


def create_random_org_traj(with_add_points=False):
    num_games = 64

    if with_add_points:
        return np.append(np.array(simulate_add_points()), (np.random.randint(0, 3, num_games) == 0))
    else:
        return np.append(np.array(0), (np.random.randint(0, 3, num_games) == 0))


# -------------------------------------------- end traj. creation ------------------------------------------------- #


# -------------------------------------------- data import starts ------------------------------------------------- #
# this will only happen once after app.py starts
df = pd.read_excel(  # "backend/database.xlsx",
    "https://github.com/MCechgh/WorldCupBettings/blob/main/backend/database.xlsx?raw=true",
    index_col=0)

tip_cols = []
score_cols = []
name_cols = []

for col_name in df.columns:
    if 'tip' in col_name[:3]:
        tip_cols.append(col_name)
        name_cols.append(col_name[4:])
    if 'score' in col_name[:5]:
        score_cols.append(col_name)

# for name, tip, score in zip(name_cols, tip_cols, score_cols):
#     print('Short check', name, tip, score)

played_matches = df[df['results'].notna()]
upcoming_matches = df[df['results'].isna()]


# -------------------------------------------- data import ends ------------------------------------------------- #

# ------------------------------- defining plots and texts starts  ------------------------------------------------- #

def plot1():
    weight_factor = np.ones(65)
    weight_factor[49:] = 2

    df_scores = df[score_cols].astype(int)

    if True:
        for n in range(100):
            df_scores[f'random_dot_org_{n}'] = create_random_org_traj()

    df_scores = pd.DataFrame(df_scores.to_numpy() * weight_factor.reshape((65, 1)), columns=df_scores.columns)

    fever_curve = df_scores.cumsum()

    fig = px.line(fever_curve, x=fever_curve.index, y=fever_curve.columns, labels={
        "value": "Score",
        "variable": "Legend"
    }, title="Score evolution")

    last_played_match = df[df['results'].notna()].index[-1] + 1
    fig.add_vline(x=last_played_match + 1, annotation_text="last played match", annotation_position="bottom right")

    fig.write_html('fun1.html')


def create_data_for_prediction():
    NTRAJ = 20000

    num_games = 16

    data = [np.append(np.array(simulate_add_points()), (np.random.randint(0, 2, num_games) == 0)) for _ in range(NTRAJ)]

    df = pd.DataFrame(data)

    df.to_excel('fun2data.xlsx')


def plot2():
    df_4prediction = pd.read_excel('fun2data.xlsx', index_col=0)

    df_4prediction_with_factor2 = copy.copy(df_4prediction)
    df_4prediction_with_factor2.iloc[:, 1:] = df_4prediction_with_factor2.iloc[:, 1:] * 2

    pred_score = df_4prediction.sum(axis=1).to_frame('pred_points')

    pred_hist = pred_score.groupby('pred_points').size() / 20000

    a = 0


if __name__ == '__main__':
    # plot1()
    # create_data_for_prediction()
    plot2()
