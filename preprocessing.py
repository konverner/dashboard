import numpy as np
from const import BANK_HOLIDAYS


def add_holiday_weekend(df):
    df['Weekend'] = np.where(df.day > 4, 1, 0)
    df['Holiday'] = df['starttime'].apply(lambda x: 1 * any([k in x for k in BANK_HOLIDAYS]))
    return df


def fahrenheit2celsius(df):
    df['temperature'] = (df['temperature'] - 32) * 5 / 9
    return df


def trip_duration_outliers(df, coef = 1.5):
    q1 = df['tripduration'].quantile(.25)
    q3 = df['tripduration'].quantile(.75)
    iqr = q3 - q1
    fltr = (df['tripduration'] >= q1 - coef * iqr) & (df['tripduration'] <= q3 + coef * iqr)
    df = df.loc[fltr]
    return df


def preprocess(df):
    df = add_holiday_weekend(df)
    df = fahrenheit2celsius(df)
    df = trip_duration_outliers(df)
    return df
