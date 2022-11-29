import numpy as np
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd


# -------------------------------------------- implement traj. ---------------------------------------------------- #
def create_random_org_traj():
    num_games = 64

    return np.append(np.array(0), (np.random.randint(0, 3, num_games) == 0))


# -------------------------------------------- end traj. creation ------------------------------------------------- #


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

# for name, tip, score in zip(name_cols, tip_cols, score_cols):
#     print('Short check', name, tip, score)

played_matches = df[df['results'].notna()]
upcoming_matches = df[df['results'].isna()]

# -------------------------------------------- data import ends ------------------------------------------------- #

# ------------------------------- defining plots and texts starts  ------------------------------------------------- #

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

fig.show()
