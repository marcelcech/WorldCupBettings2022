import pandas as pd


def _init_excel():
    df = pd.DataFrame(index=range(64), columns=['match', 'results', 'tip Marcel', 'score Marcel'])
    df.to_excel('database_new.xlsx')


def eval(result: str):
    if type(result) == str:
        result = result.split('-')
        if int(result[0]) > int(result[1]):
            return 1
        elif int(result[0]) < int(result[1]):
            return -1
        else:
            return 0
    else:
        return result


def _update_excel():
    df = pd.read_excel('database.xlsx', index_col=0)

    tip_cols = []
    score_cols = []

    # update results from real score
    df['results'] = df['clear text results'].apply(eval)

    for col_name in df.columns:
        if 'tip' in col_name[:3]:
            tip_cols.append(col_name)
        if 'score' in col_name[:5]:
            score_cols.append(col_name)

    for tip, score in zip(tip_cols, score_cols):
        print('Short check', tip, score)
        df[score] = (df['results'] - df[tip]) < 1e-9

    df.to_excel('database.xlsx')


if __name__ == '__main__':
    _update_excel()
