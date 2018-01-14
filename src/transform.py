from dfply import *

@pipe
def narep(df, val=0):
    df = df.fillna(val)
    return df

@dfpipe
def do(df, todo):
    return todo
