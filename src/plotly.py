from dfply import *
import warnings
import numpy as np

import plotly.offline as offline
from plotly.graph_objs import Scatter, Annotation, Heatmap, Trace, Bar

def _solve_intention(obj, df):
    if isinstance(obj, dict):
        return {k: _solve_intention(v, df) for k, v in obj.items()}
    elif isinstance(obj, base.Intention):
        return obj.evaluate(df).tolist()
    else:
        return obj

@pipe
def plot_ly(df):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        df.plotly = {'data': [], 'layout': {}}
        df._metadata.append("plotly")
    return df

@pipe
def add_trace(df, *args, **kwargs):
    kw = _solve_intention(kwargs, df)
    df.plotly['data'].append(Trace(*args, **kw))
    return df

@pipe
def _add_scatter(df, *args, **kwargs):
    kw = _solve_intention(kwargs, df)
    df.plotly['data'].append(Scatter(*args, **kw))
    return df

_which = lambda lst:list(np.where(lst)[0])

@pipe
def add_scatter(df, *args, **kwargs):
    if "color" in kwargs:
        uniquecolors = kwargs['color'].evaluate(df).drop_duplicates().tolist()
        df_color = kwargs['color'].evaluate(df).tolist()
        kw = kwargs
        del kw['color']
        for c in uniquecolors:
            kw['name'] = c
            df.plotly = (df.iloc[_which(list(map(lambda x: x == c, df_color))),:] >> 
                _add_scatter(*args, **kwargs)).plotly
        return df
    else:
        return df >> _add_scatter(*args, **kwargs)

@pipe
def add_bar(df, *args, **kwargs):
    kw = _solve_intention(kwargs, df)
    df.plotly['data'].append(Bar(*args, **kw))
    return df

@pipe
def add_heatmap(df, *args, **kwargs):
    kw = _solve_intention(kwargs, df)
    df.plotly['data'].append(Heatmap(*args, **kw))
    return df


@pipe
def add_annotations(df, *args, **kwargs):
    kw = solve_intention(kwargs, df)
    if 'annotations' in df.plotly['layout']:
        df.plotly['layout']['annotations'].append(Annotation(*args, **kw))
    else:
        df.plotly['layout']['annotations'] = [Annotation(*args, **kw)]
    return df

@pipe
def layout(df, *args,  **kwargs):
    df.plotly['layout'].update(_solve_intention(kwargs, df))
    return df

@pipe
def show(df):
    offline.iplot(df.plotly, show_link=False)

@pipe
def export(df, filename, format="png"):
    offline.plot(df.plotly, filename=filename, image=format)

