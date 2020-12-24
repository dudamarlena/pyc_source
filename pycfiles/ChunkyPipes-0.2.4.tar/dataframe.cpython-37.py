# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chunkypandas\core\dataframe.py
# Compiled at: 2019-12-23 18:56:16
# Size of source mod 2**32: 3308 bytes
__doc__ = '\ndataframe.py\nwritten in Python3\nauthor: C. Lockhart <chris@lockhartlab.org>\n'
from .base import ChunkyBase
from .series import ChunkySeries
import os, tempfile

class ChunkyDataFrame(ChunkyBase):
    """ChunkyDataFrame"""

    def __init__(self, path=None, ext=None, chunksize=1000, index_col=0):
        """
        Initialize class instance

        Parameters
        ----------
        path : str
            Location of file
        ext : str
            (Optional) File type of `path`
        chunksize : int
            The size of chunks to read in and handle in memory (Default: 1000)
        index_col : int
            Location of index in `path`. `None` means no index. (Default: 0)
        """
        super().__init__(path, ext, chunksize, index_col)

    def __getitem__(self, column):
        return self._column_to_series(str(column))

    def _column_to_series(self, column):
        """
        Convert *column* to `chunkypandas.Series`

        Parameters
        ----------
        column : str
            Column to convert to Series

        Returns
        -------
        chunkypandas.Series
        """
        path = os.path.join(tempfile.gettempdir(), 'chunkypandas_' + os.urandom(24).hex() + '.csv')

        def _compute(chunk):
            header = False if os.path.exists(path) else True
            chunk[[column]].iloc[:, 0].to_csv(path, index=True, header=header, mode='a+')

        self.compute_combine_reduce(compute=_compute, combine='empty', reduce='empty')
        return ChunkySeries(path, ext='csv', chunksize=(self.chunksize), index_col=0)

    def pivot_table(self, aggfunc='mean', *args, **kwargs):
        """
        Pivot table is tricky because chunks might have different values. We need to utilize the first chunks bins for
        all other chunks (?)

        Parameters
        ----------
        aggfunc
        args
        kwargs

        Returns
        -------

        """

        def _compute(chunk):
            if aggfunc == 'mean':
                result = (
                 (chunk.pivot_table)(args, aggfunc='sum', **kwargs),
                 (chunk.pivot_table)(args, aggfunc='count', **kwargs))
            else:
                result = (chunk.pivot_table)(args, aggfunc=aggfunc, **kwargs)
            return result

        def _reduce(result):
            if aggfunc == 'mean':
                result = result[0] / result[1]
            return result

        return self.compute_combine_reduce(compute=_compute, combine='add', reduce=_reduce)