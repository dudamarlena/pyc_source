# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dtale/cli/loaders/arctic_loader.py
# Compiled at: 2020-04-18 12:53:10
from logging import getLogger
import pandas as pd
from dtale.app import show
from dtale.cli.clickutils import get_loader_options
logger = getLogger(__name__)
NOW = pd.Timestamp('now').strftime('%Y%m%d')
LOADER_KEY = 'arctic'
LOADER_PROPS = [
 dict(name='host', help='arctic hostname'),
 dict(name='library', help='library within --arctic-host'),
 dict(name='node', help='node within --arctic-library'),
 dict(name='start', help=('start-date of range to load if reading from ChunkStore (EX: {})').format(NOW)),
 dict(name='end', help=('end-date of range to load if reading from ChunkStore (EX: {})').format(NOW))]

def show_loader(**kwargs):
    return show(data_loader=(lambda : loader_func(**kwargs)), **kwargs)


def loader_func(**kwargs):
    try:
        from arctic import Arctic
        from arctic.store.versioned_item import VersionedItem
    except ImportError:
        raise ImportError('In order to use the arctic loader you must install arctic!')

    host = Arctic(kwargs.get('host'))
    lib = host.get_library(kwargs.get('library'))
    read_kwargs = {}
    start, end = (kwargs.get(p) for p in ['start', 'end'])
    if start and end:
        read_kwargs['chunk_range'] = pd.date_range(start, end)
    data = lib.read(kwargs.get('node'), **read_kwargs)
    if isinstance(data, VersionedItem):
        data = data.data
    return data


def find_loader(kwargs):
    """
    Arctic implementation of data loader which will return a function if any of the
    `click` options based on LOADER_KEY & LOADER_PROPS have been used, otherwise return None

    :param kwargs: Optional keyword arguments to be passed from `click`
    :return: data loader function for arctic implementation
    """
    arctic_opts = get_loader_options(LOADER_KEY, kwargs)
    if len([ f for f in arctic_opts.values() if f ]):

        def _arctic_loader():
            return loader_func(**arctic_opts)

        return _arctic_loader
    else:
        return