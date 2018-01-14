from dfply import *

@make_symbolic
def as_character(col):
    return col.apply(str)

@make_symbolic
def which(lst):
    return list(np.where(lst)[0])

@make_symbolic
def round_to(series, step=1):
    return (series/step).round()*step


