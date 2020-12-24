# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chunkypandas\core\series.py
# Compiled at: 2019-12-23 17:49:18
# Size of source mod 2**32: 1869 bytes
"""
series.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""
from .base import ChunkyBase
import numpy as np, pandas as pd
from typelike import ListLike, NumberLike

class ChunkySeries(ChunkyBase):
    __doc__ = "\n    Tired of memory-intensive pandas objects? Look no further! With ``ChunkySeries``, you pretend like you're still\n    using pandas but utilize your hard-drive instead of memory\n    "

    def __init__(self, path, ext=None, chunksize=1000, index_col=0):
        """
        Initialize class instance

        Parameters
        ----------
        path : str
            Location to data
        ext : str
            (Optional) Data extension. If not provided, guessed
        chunksize : int
            Size of data chunks to read in (DEfault: 1000)
        index_col : int
            Location of index. None means no index (Default: 0)
        """
        super().__init__(path, ext, chunksize, index_col)

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.sub(other)

    def sub(self, other):
        """
        Subtract from the ChunkySeries

        Currently supported are constant values and other ChunkySeries instances

        Parameters
        ----------
        other : NumberLike or ChunkySeries
            Something to add to this instance of ChunkySeries

        Returns
        -------
        ChunkySeries
            This instance subtracted by *other*
        """
        return self.compute_combine_reduce(compute='sub', combine='concat', other=other)