# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/multi.py
# Compiled at: 2020-05-04 13:32:17
# Size of source mod 2**32: 2347 bytes
"""
buzz: multiprocessing helpers
"""
import multiprocessing, os
from joblib import delayed
from .utils import _get_tqdm, _to_df, _tqdm_close, _tqdm_update

def how_many(multiprocess):
    """
    Get number of processes, or False

    Hardest utility ever written.
    """
    if os.name == 'nt':
        return 1
    if multiprocess is True:
        multiprocess = multiprocessing.cpu_count()
    if multiprocess in {0, 1, None}:
        multiprocess = 1
    return multiprocess


@delayed
def load(files, position, **kwargs):
    """
    Picklable loader for multiprocessing
    """
    kwa = dict(ncols=120,
      unit='chunk',
      desc='Loading',
      position=position,
      total=(len(files)))
    t = (_get_tqdm())(**kwa)
    out = []
    for file in files:
        out.append(_to_df(corpus=file, _complete=False, **kwargs))
        _tqdm_update(t)

    _tqdm_close(t)
    return out


@delayed
def read(files, position):
    """
    Picklable reader for multiprocessing (for unparsed corpora)
    """
    kwa = dict(ncols=120,
      unit='chunk',
      desc='Reading',
      position=position,
      total=(len(files)))
    t = (_get_tqdm())(**kwa)
    out = []
    for file in files:
        with open(file.path, 'r') as (fo):
            out.append(fo.read())
        _tqdm_update(t)

    _tqdm_close(t)
    return out


@delayed
def search(corpus, queries, position, **kwargs):
    """
    Picklable searcher for multiprocessing

    No need for progress bar  because it is in depgrep
    """
    out = []
    for query in queries:
        res = (corpus.depgrep)(query, position=position, **kwargs)
        if res is not None:
            res.empty or out.append(res)

    return out


@delayed
def parse(paths, position, save_as, corpus_name, language, constituencies, speakers):
    """
    Parse using multiprocessing, chunks of paths
    """
    from .parse import _process_string
    kwa = dict(ncols=120,
      unit='file',
      desc='Parsing',
      position=position,
      total=(len(paths)))
    t = (_get_tqdm())(**kwa)
    for path in paths:
        with open(path, 'r') as (fo):
            plain = fo.read().strip()
        _process_string(plain, path, save_as, corpus_name, language, constituencies, speakers)
        _tqdm_update(t)

    _tqdm_close(t)