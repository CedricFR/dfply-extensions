from dfply import *

@pipe
def nrow(df):
    return df.shape[0]

@pipe
def ncol(df):
    return df.shape[1]

