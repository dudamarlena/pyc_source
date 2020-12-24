# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/conc.py
# Compiled at: 2019-08-24 15:46:35
# Size of source mod 2**32: 2653 bytes
import pandas as pd
from pandas import option_context
from .constants import CONLL_COLUMNS
from .utils import _auto_window, _make_match_col
from .views import _tabview
pd.options.mode.chained_assignment = None

class Concordance(pd.DataFrame):
    __doc__ = '\n    A dataframe holding left, match and right columns, plus optional metadata\n    '
    _internal_names = pd.DataFrame._internal_names
    _internal_names_set = set(_internal_names)
    _metadata = [
     'reference']
    reference = None

    def __init__(self, data, reference=None, *args, **kwargs):
        (super().__init__)(data, **kwargs)
        self.reference = reference

    @property
    def _constructor(self):
        return Concordance

    def view(self, *args, **kwargs):
        return _tabview(self, self.reference, *args, **kwargs)

    def __repr__(self):
        cols = [
         'left', 'match', 'right']
        if 'speaker' in self.columns:
            if self['speaker'][0]:
                cols.append('speaker')
        with option_context('display.max_colwidth', 200):
            return str(self[cols])


def _apply_conc(line, allwords, window):
    middle, n = line['_match'], line['_n']
    start = max(n - window[0], 0)
    end = min(n + window[1], len(allwords) - 1)
    left = ' '.join(allwords[start:n])[-window[0]:]
    right = ' '.join(allwords[n + 1:end])[:window[1]]
    series = pd.Series([left, middle, right])
    series.names = ['left', 'match', 'right']
    return series


def _concordance(data_in, reference, show=[
 'w'], n=100, window='auto', metadata=True, preserve_case=True):
    """
    Generate a concordance
    """
    n = max(n, len(data_in))
    if window == 'auto':
        window = _auto_window()
    if isinstance(window, int):
        window = [
         window, window]
    data_in['_match'] = _make_match_col(data_in, show, preserve_case=preserve_case)
    df = pd.DataFrame(data_in).reset_index()
    finished = df.apply(_apply_conc,
      axis=1, allwords=(reference['w'].values), window=window)
    finished.columns = [
     'left', 'match', 'right']
    finished = finished[['left', 'match', 'right']]
    cnames = list(df.columns)
    if metadata is True:
        metadata = [i for i in cnames if i not in CONLL_COLUMNS]
    if metadata:
        met_df = df[metadata]
        finished = pd.concat([finished, met_df], axis=1, sort=False)
    finished = finished.drop([
     '_match', '_n', 'sent_len', 'parse'],
      axis=1, errors='ignore')
    return Concordance(finished, reference=data_in)