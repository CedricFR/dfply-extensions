from dfply import *

# Check & change type

@make_symbolic
def as_character(col):
    return col.apply(str)

@make_symbolic
def is_na(x):
    return np.isnan(x)

# Other

@make_symbolic
def which(lst):
    return list(np.where(lst)[0])

@make_symbolic
def round_to(series, step=1):
    return (series/step).round()*step

@make_symbolic
def pmin(a,b):
    return np.minimum(a,b)
