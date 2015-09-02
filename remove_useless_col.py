import pandas as pd
import numpy as np
train = pd.read_csv("data/train.csv")
test  = pd.read_csv("data/test.csv")


def drop_useless_col(df, cols):
    useless_col = []
    num_features = df.select_dtypes(exclude=['object']).columns
    cat_features = df.select_dtypes(include=['object']).columns
    for col in cols:
        #if col == 'VAR_0213':
        unique_count = len(pd.unique(df[col].values.ravel()))
        if unique_count == 2:
            if pd.isnull(df[col].values).any():
                useless_col.append(col)
                print col

        if unique_count == 1:
            useless_col.append(col)
            print col
    return df.drop(useless_col, axis =1)

cols = train.drop(['ID', 'target'], axis =1).columns
train = drop_useless_col(train, cols)
cols = test.drop(['ID'], axis =1).columns
test = drop_useless_col(test, cols)

train.to_csv('data/train_v1.csv', index=False)
test.to_csv('data/test_v1.csv', index=False)
