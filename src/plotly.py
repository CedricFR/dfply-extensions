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

@dfpipe
def add_trace(df, *args, **kwargs):
    df.plotly['data'].append(Trace(*args, **kwargs))
    return df

@dfpipe
def _add_scatter(df, *args, **kwargs):
    df.plotly['data'].append(Scatter(*args, **kwargs))
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

@dfpipe
def add_bar(df, *args, **kwargs):
    df.plotly['data'].append(Bar(*args, **kwargs))
    return df

@dfpipe
def add_heatmap(df, *args, **kwargs):
    df.plotly['data'].append(Heatmap(*args, **kwargs))
    return df


@dfpipe
def add_annotations(df, *args, **kwargs):
    if 'annotations' in df.plotly['layout']:
        df.plotly['layout']['annotations'].append(Annotation(*args, **kwargs))
    else:
        df.plotly['layout']['annotations'] = [Annotation(*args, **kwargs)]
    return df

@dfpipe
def layout(df, *args,  **kwargs):
    df.plotly['layout'].update(kwargs)
    return df

@pipe
def show(df):
    offline.iplot(df.plotly, show_link=False)

@pipe
def export(df, filename, format="png"):
    offline.plot(df.plotly, filename=filename, image=format)

