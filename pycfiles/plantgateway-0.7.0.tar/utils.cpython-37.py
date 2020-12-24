# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plantflow/utils.py
# Compiled at: 2020-01-29 12:46:28
# Size of source mod 2**32: 1438 bytes
from matplotlib import colors
from itertools import cycle
import numpy as np, pandas as pd

def my_colors():
    """
    return a tableau colors iterable
    """
    tab = cycle(colors.TABLEAU_COLORS)
    return tab


def make_pdf(dist, params, size=10000):
    """Generate distributions's Probability Distribution Function """
    arg = params[:-2]
    loc = params[(-2)]
    scale = params[(-1)]
    start = (dist.ppf)(0.01, *arg, **{'loc':loc,  'scale':scale}) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = (dist.ppf)(0.99, *arg, **{'loc':loc,  'scale':scale}) if arg else dist.ppf(0.99, loc=loc, scale=scale)
    x = np.linspace(start, end, size)
    y = (dist.pdf)(x, *arg, **{'loc':loc,  'scale':scale})
    pdf = pd.Series(y, x)
    return pdf


def boxplot_sorted(df, by, column, rot=0):
    df2 = pd.DataFrame({col:vals[column] for col, vals in df.groupby(by)})
    meds = df2.median().sort_values()
    return df2[meds.index].boxplot(rot=rot, return_type='axes', vert=False)