import pandas as pd

def preprocess(df):
    df = pd.concat([df, pd.get_dummies(df['medal_type'])], axis=1)
    return df