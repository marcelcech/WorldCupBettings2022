import pandas as pd


def _init_excel():
    df = pd.DataFrame(index=range(64), columns=['match', 'results', 'tip Marcel', 'score Marcel'])
    df.to_excel('database_new.xlsx')


def _update_excel():
    df = pd.read_excel('database.xlsx', index_col=0)

    tip_cols = []
    score_cols = []

    for col_name in df.columns:
        if 'tip' in col_name[:3]:
            tip_cols.append(col_name)
        if 'score' in col_name[:5]:
            score_cols.append(col_name)

    for tip, score in zip(tip_cols, score_cols):
        print('Short check', tip, score)
        df[score] = (df['results'] == df[tip])

    df.to_excel('database.xlsx')


if __name__ == '__main__':
    _update_excel()
