import pandas as pd
import numpy as np
import datetime
import time
train = pd.read_csv("data/train_v1.csv")
test  = pd.read_csv("data/test_v1.csv")

date_cols = ['VAR_0073','VAR_0075','VAR_0166','VAR_0168','VAR_0169','VAR_0176','VAR_0178','VAR_0179','VAR_0204', 'VAR_0217']


def process_date(train, test, cols):
    '''
    Extract the year, month and day from the date
    '''
    # Functions to extract year, month and day from dataset
    def create_year(x):
        return str(x.split(':')[0])[:2]
    def create_month(x):
        return str(x.split(':')[0])[2:5]
    def create_day(x):
        return str(x.split(':')[0])[5:]

    for ds in [train, test]:
        for col in cols:
            ds[col].fillna('00JAN00:00:00:00', inplace=True)
            ds[col+'_year' ] = ds[col].apply(create_year)
            ds[col+'_month'] = ds[col].apply(create_month)
            ds[col+'_day'  ] = ds[col].apply(create_day)
process_date(train, test, date_cols)
train.to_csv('data/train_v2.csv', index=False)
test.to_csv('data/test_v2.csv', index=False)


