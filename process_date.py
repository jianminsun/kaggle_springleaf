import pandas as pd
import numpy as np
import datetime
import time
train = pd.read_csv("data/train_v1.csv")
test  = pd.read_csv("data/test_v1.csv")

date_cols = ['VAR_0073','VAR_0075','VAR_0166','VAR_0168','VAR_0169','VAR_0176','VAR_0178','VAR_0179','VAR_0204', 'VAR_0217']
monthDict={'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5, 'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9, 'OCT':10, 'NOV':11, 'DEC':12}


def process_date(train, test, cols):
    '''
    Extract the year, month and day from the date
    '''
    # Functions to extract year, month and day from dataset
    def create_day(x):
        return str(x.split(':')[0])[:2]
    def create_month(x):
        return str(x.split(':')[0])[2:5]
    def create_year(x):
        return str(x.split(':')[0])[5:]
    def create_days_diff(x):
        day = int(x.split(':')[0][:2])
        month = int(monthDict[str(x.split(':')[0])[2:5]])
        year = int(x.split(':')[0][5:])+2000
        try:
            days_diff = (datetime.date(year, month, day) - datetime.date(11, 01, 01)).days
        except:
            print year, month, day, x
        return days_diff
    for ds in [train, test]:
        for col in cols:
            ds[col].fillna('01JAN11:00:00:00', inplace=True)
            #ds[col+'_year' ] = ds[col].apply(create_year)
            #ds[col+'_month'] = ds[col].apply(create_month)
            #ds[col+'_day'  ] = ds[col].apply(create_day)
            ds[col+'_days_diff'] = ds[col].apply(create_days_diff)
            ds.drop(col, axis=1, inplace=True)
        for i, col1 in enumerate(cols):
            for col2 in cols[i+1:]:
                #print col1, col2
                ds[col1+'_days_diff_'+col2] = ds[col1+'_days_diff'] - ds[col2+'_days_diff']


process_date(train, test, date_cols)
train.to_csv('data/train_v2.csv', index=False)
test.to_csv('data/test_v2.csv', index=False)


