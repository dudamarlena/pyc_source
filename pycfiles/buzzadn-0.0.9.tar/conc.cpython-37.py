# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/conc.py
# Compiled at: 2020-05-03 13:12:48
# Size of source mod 2**32: 2401 bytes
import pandas as pd
from .constants import CONLL_COLUMNS
from .utils import _auto_window, _make_match_col
from .views import _tabview

class Concordance(pd.DataFrame):
    """Concordance"""
    _internal_names = pd.DataFrame._internal_names
    _internal_names_set = set(_internal_names)
    _metadata = [
     'reference']
    reference = None

    def __init__(self, data, reference=None):
        super().__init__(data)
        self.reference = reference

    @property
    def _constructor(self):
        return Concordance

    def view(self, *args, **kwargs):
        return _tabview(self, self.reference, *args, **kwargs)


def _get_right(n, allwords, window):
    """
    For df.apply(), generate right

    This needs to be performant.
    """
    end = min(n + window[1], len(allwords) - 1)
    return ' '.join(allwords[n + 1:end])[:window[1]]


def _get_left(n, allwords, window):
    """
    For df.apply(), generate left

    This needs to be performant.
    """
    return ' '.join(allwords[max(n - window[0], 0):n])[-window[0]:]


def _concordance(data_in, reference, show=[
 'w'], n=-1, window='auto', metadata=True, preserve_case=True, preserve_index=False):
    """
    Generate a concordance
    """
    if n:
        if n > 0:
            data_in = data_in.iloc[:n]
    else:
        if window == 'auto':
            window = _auto_window()
        if isinstance(window, int):
            window = [
             window, window]
        data_in = preserve_index or data_in.reset_index()
    matches = _make_match_col(data_in, show, preserve_case=preserve_case)
    match_indices = data_in['_n']
    words = reference['w'].values
    apply_data = dict(allwords=words, window=window)
    left = (match_indices.apply)(_get_left, **apply_data)
    right = (match_indices.apply)(_get_right, **apply_data)
    left.name, matches.name, right.name = ('left', 'match', 'right')
    ignores = [
     '_match', '_n', 'sent_len', 'parse', 'text']
    conc = pd.concat([left, matches, right], axis=1)
    if metadata is True:
        skips = CONLL_COLUMNS + ignores
        metadata = [i for i in list(data_in.columns) if i not in skips]
    if metadata:
        conc = conc.join(data_in[metadata])
    return Concordance(conc, reference=data_in)