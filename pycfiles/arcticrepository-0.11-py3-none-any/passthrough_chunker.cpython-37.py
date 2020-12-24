# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/chunkstore/passthrough_chunker.py
# Compiled at: 2018-11-17 20:47:49
# Size of source mod 2**32: 1647 bytes
from pandas import DataFrame, Series
from ._chunker import Chunker

class PassthroughChunker(Chunker):
    TYPE = 'passthru'

    def to_chunks(self, df, **kwargs):
        """
        pass thru chunker of the dataframe/series

        returns
        -------
        ('NA', 'NA', 'NA', dataframe/series)
        """
        if len(df) > 0:
            yield (
             'NA', 'NA', 'NA', df)

    def to_range(self, start, end):
        """
        returns a RangeObject from start/end sentinels.

        returns
        -------
        string
        """
        return 'NA'

    def chunk_to_str(self, chunk_id):
        """
        Converts parts of a chunk range (start or end) to a string

        returns
        -------
        string
        """
        return 'NA'

    def to_mongo(self, range_obj):
        """
        returns mongo query against range object.
        since range object is not valid, returns empty dict

        returns
        -------
        string
        """
        return {}

    def filter(self, data, range_obj):
        """
        ensures data is properly subset to the range in range_obj.
        since range object is not valid, returns data

        returns
        -------
        data
        """
        return data

    def exclude(self, data, range_obj):
        """
        Removes data within the bounds of the range object.
        Since range object is not valid for this chunk type,
        returns nothing

        returns
        -------
        empty dataframe or series
        """
        if isinstance(data, DataFrame):
            return DataFrame()
        return Series()