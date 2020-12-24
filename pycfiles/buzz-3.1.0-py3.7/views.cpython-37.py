# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/views.py
# Compiled at: 2019-09-05 14:05:50
# Size of source mod 2**32: 9664 bytes
"""
in buzz, searches result in corpus subsets. views represent subsets as stats,
or as concordance lines, or as figures...
"""
import math, numpy as np, pandas as pd
from .utils import _auto_window, _make_match_col
from .tabview import view

def _get_widths(df, is_conc, window):
    tot = len(df.columns) + len(df.index.names)
    aligns = [True] * tot
    truncs = [False] * tot
    widths = [5]
    if not is_conc:
        widths = [
         20] * len(df.index.names)
    for i, col_name in enumerate(df.columns):
        if not is_conc:
            widths.append(8)
        else:
            if is_conc:
                if col_name == 'left':
                    widths.append(window[0])
                    truncs[i + len(df.index.names)] = True
            if is_conc and col_name == 'right':
                widths.append(window[1])
                aligns[i + len(df.index.names)] = False
            elif is_conc:
                if col_name == 'match':
                    mx = df[col_name].astype(str).str.len().max() + 1
                    mx = min(15, mx)
                    widths.append(mx)
                    aligns[i + len(df.index.names)] = False
        if is_conc:
            mx = df[col_name].astype(str).str.len().max() + 1
            if mx > 10:
                mx = 10
            widths.append(mx)

    return (
     aligns, truncs, widths)


def _tabview(df, reference, window='auto', **kwargs):
    """
    Show concordance in interactive cli view
    """
    from .conc import Concordance
    is_conc = type(df) == Concordance
    if isinstance(df.index, pd.MultiIndex):
        index_as_iterable = list(zip(*df.index.to_series()))
        widths = list()
        for index in index_as_iterable:
            biggest = max([len(str(x)) for x in index])
            if biggest < 10:
                widths.append(biggest)
            else:
                widths.append(10)

    else:
        widths = [
         5]
    if isinstance(window, int):
        window = [
         window, window]
    else:
        if window == 'auto':
            window = _auto_window()
        else:
            window = list(window)
    if is_conc:
        window[0] = max(df['left'].str.len().max(), window[0])
        window[1] = max(df['right'].str.len().max(), window[1])
    aligns, truncs, widths = _get_widths(df, is_conc, window)
    view_style = dict(column_widths=widths, reference=reference, df=df)
    if 'align_right' not in kwargs:
        view_style['align_right'] = aligns
    if 'trunc_left' not in kwargs:
        view_style['trunc_left'] = truncs
    view(df, **view_style)


def _lingres(ser, index):
    """
    Appliable stats calculation
    """
    from scipy.stats import linregress
    ix = [
     '_slope', '_intercept', '_r', '_p', '_stderr']
    return pd.Series((linregress(index, ser.values)), index=ix)


def _sort(df, by=False, keep_stats=False, remove_above_p=False):
    """
    Sort results, potentially using scipy's linregress
    """
    stat_field = [
     '_slope', '_intercept', '_r', '_p', '_stderr']
    easy_sorts = ['total', 'infreq', 'name', 'most', 'least', 'reverse']
    stat_sorts = ['increase', 'decrease', 'static', 'turbulent']
    options = stat_field + easy_sorts + stat_sorts
    by_convert = {'most':'total', 
     True:'total',  'least':'infreq'}
    by = by_convert.get(by, by)
    if keep_stats or by in stat_field + stat_sorts:
        n_column = list(range(len(df)))
        try:
            df.index = df.index.astype(int)
        except Exception:
            try:
                df.index = df.index.astype(object)
            except Exception:
                pass

        stats = df.apply(_lingres, axis=0, index=n_column)
        df = df.append(stats)
        df = df.replace([np.inf, -np.inf], 0.0)
    if by == 'name':
        df = df.reindex((sorted(df.columns)), axis=1)
    else:
        if by in {'infreq', 'total'}:
            ascending = by != 'total'
            df = df[list(df.sum().sort_values(ascending=ascending).index)]
        else:
            if by == 'reverse':
                df = df.loc[:, ::-1]
            elif not by in stat_field:
                if by not in options:
                    asc = False if (by is True or by in {'most', 'total'}) else True
                    df = df.T.sort_values(by=by, ascending=asc).T
                if '_slope' in df.index:
                    slopes = df.loc['_slope']
                    if by == 'increase':
                        std = slopes.sort_values(ascending=False)
                        df = df[std.index]
                    else:
                        if by == 'decrease':
                            std = slopes.sort_values(ascending=True)
                            df = df[std.index]
                        else:
                            if by == 'static':
                                std = slopes.abs().sort_values(ascending=True)
                                df = df[std.index]
                            else:
                                if by == 'turbulent':
                                    std = slopes.abs().sort_values(ascending=False)
                                    df = df[std.index]
                    if remove_above_p is not False:
                        if remove_above_p > 0:
                            df = df.T
                            df = df[(df['_p'] <= remove_above_p)]
                            df = df.T
                df = keep_stats or df.drop(stat_field, axis=0, errors='ignore')
            else:
                df.index = [i.lstrip('_') if i in stat_field else i for i in list(df.index)]
            return df


def _log_likelihood(word_in_ref, word_in_target, ref_sum, target_sum):
    """
    calculate log likelihood keyness
    """
    neg = word_in_target / float(target_sum) < word_in_ref / float(ref_sum)
    ref_targ = float(word_in_ref) + float(word_in_target)
    ref_targ_sum = float(ref_sum) + float(target_sum)
    E1 = float(ref_sum) * (ref_targ / ref_targ_sum)
    E2 = float(target_sum) * (ref_targ / ref_targ_sum)
    logaE1 = 0 if not word_in_ref else math.log(word_in_ref / E1)
    logaE2 = 0 if not word_in_target else math.log(word_in_target / E2)
    score = float(2 * (word_in_ref * logaE1 + word_in_target * logaE2))
    if neg:
        score = -score
    return score


def _perc_diff(word_in_ref, word_in_target, ref_sum, target_sum):
    """calculate using perc diff measure"""
    norm_target = float(word_in_target) / target_sum
    norm_ref = float(word_in_ref) / ref_sum
    if norm_ref == 0:
        norm_ref = 1e-26
    return (norm_target - norm_ref) * 100.0 / norm_ref


def _make_keywords(subcorpus, reference, ref_sum, target_sum, measure):
    points = [(reference.get(name, 0), count, ref_sum, target_sum) for name, count in subcorpus.items()]
    return [measure(*arg) for arg in points]


def _table(dataset, subcorpora=[
 'file'], show=[
 'w'], preserve_case=False, sort='total', relative=False, keyness=False, remove_above_p=False, multiindex_columns=False, keep_stats=False, **kwargs):
    """
    Generate a result table view from Results, or a Results-like DataFrame
    """
    from .table import Table
    df, reference = dataset, dataset.reference
    if not isinstance(show, list):
        show = [
         show]
    if not isinstance(subcorpora, list):
        subcorpora = [
         subcorpora]
    for to_show in show:
        if not to_show.startswith(('+', '-')):
            continue
        df[to_show] = reference[to_show[2:]].shift(-int(to_show[1]))

    if remove_above_p is True:
        remove_above_p = 0.05
    df['_match'] = _make_match_col(df, show, preserve_case)
    if reference is not None:
        reference['_match'] = df['_match']
    df['_count'] = 1
    table = df.pivot_table(index=subcorpora,
      columns='_match',
      values='_count',
      aggfunc=sum)
    table = table.fillna(0)
    table = Table(table, reference=reference)
    table = table.relative(relative) if relative is not False else table.astype(int)
    if keyness:
        if reference is None:
            warn = 'Warning: no reference corpus supplied. Using result frame as reference corpus'
            print(warn)
            reference = df
        ref = reference['_match'].value_counts()
        kwa = dict(axis=0,
          reference=ref,
          measure=(dict(ll=_log_likelihood, pd=_perc_diff).get(keyness, _log_likelihood)),
          ref_sum=(reference.shape[0]),
          target_sum=(table.shape[0]))
        applied = (table.T.apply)(_make_keywords, **kwa).T
        top = applied.abs().sum().sort_values(ascending=False)
        table = applied[top.index]
    if sort:
        if not keyness:
            sorts = dict(by=sort, keep_stats=keep_stats, remove_above_p=remove_above_p)
            table = (table.sort)(**sorts)
    if multiindex_columns and len(show) > 1:
        table.columns = [i.split('/') for i in table.columns.names]
        table.columns.names = table.columns.names[0].split('/')
    else:
        table.columns.name = '/'.join(show)
    df.drop(['_match', '_count'], axis=1, inplace=True, errors='ignore')
    if reference is not None:
        reference.drop('_match', axis=1, inplace=True, errors='ignore')
    return table