# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jess/.local/conda/lib/python3.6/site-packages/earthchem/geochem.py
# Compiled at: 2018-06-24 21:43:54
# Size of source mod 2**32: 1547 bytes
import pandas as pd, periodictable as pt

def common_elements(cutoff=92, output='formula'):
    """
    Provides a list of elements up to a particular cutoff (default: including U)
    Output options are 'formula', or strings.
    """
    elements = [el for el in pt.elements if not (el.__str__() == 'n' or el.number > cutoff)]
    if not output == 'formula':
        elements = [el.__str__() for el in elements]
    return elements


def REE(output='formula', include_extras=False):
    """
    Provides the list of Rare Earth Elements
    Output options are 'formula', or strings.

    Todo: add include extras such as Y.
    """
    elements = [
     'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd',
     'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
    if output == 'formula':
        elements = [getattr(pt, el) for el in elements]
    return elements


def to_molecular(df: pd.DataFrame, renorm=True):
    """
    Converts mass quantities to molar quantities of the same order.
    E.g.:
    mass% --> mol%
    mass-ppm --> mol-ppm
    """
    MWs = [pt.formula(c).mass for c in df.columns]
    if renorm:
        return renormalise(df.div(MWs))
    else:
        return df.div(MWs)


def to_weight(df: pd.DataFrame, renorm=True):
    """
    Converts molar quantities to mass quantities of the same order.
    E.g.:
    mol% --> mass%
    mol-ppm --> mass-ppm
    """
    MWs = [pt.formula(c).mass for c in df.columns]
    if renorm:
        return renormalise(df.multiply(MWs))
    else:
        return df.multiply(MWs)