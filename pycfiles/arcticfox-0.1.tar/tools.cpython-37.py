# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/chunkstore/tools/tools.py
# Compiled at: 2019-02-02 17:02:31
# Size of source mod 2**32: 1508 bytes
from itertools import groupby
import pymongo
from arctic.chunkstore.chunkstore import SYMBOL, SEGMENT, START

def segment_id_repair(library, symbol=None):
    """
    Ensure that symbol(s) have contiguous segment ids

    Parameters
    ----------
    library: arctic library
    symbol: None, str, list of str
        None: all symbols
        str: single symbol
        list: list of symbols

    Returns
    -------
    list of str - Symbols 'fixed'
    """
    ret = []
    if symbol is None:
        symbol = library.list_symbols()
    elif not isinstance(symbol, list):
        symbol = [
         symbol]
    by_segment = [(START, pymongo.ASCENDING),
     (
      SEGMENT, pymongo.ASCENDING)]
    for sym in symbol:
        cursor = library._collection.find({SYMBOL: sym}, sort=by_segment)
        for _, segments in groupby(cursor, key=(lambda x: (
         x[START], x[SYMBOL]))):
            segments = list(segments)
            if segments[0][SEGMENT] == -1:
                library._collection.delete_many({SYMBOL: sym, START: segments[0][START]})
                for index, seg in enumerate(segments):
                    seg[SEGMENT] = index

                library._collection.insert_many(segments)
                ret.append(sym)

    return ret