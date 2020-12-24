# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/UNC Drive/pymemsci/membrane_toolkit/pipeline/stores.py
# Compiled at: 2020-05-10 12:19:31
# Size of source mod 2**32: 799 bytes
from maggma.stores import MemoryStore
from pandas import DataFrame

class PandasStore(MemoryStore):
    __doc__ = '\n    Store that creates pandas dataframes from parsed data. At present this is just a\n    lightweighte extension of MemoryStore.\n    '

    def __init__(self, key):
        """
        Args:
            key: record key.
        """
        super().__init__(key=key)

    def as_df(self, drop_cols=[
 '_id', 'state_hash']):
        """
        Return a Pandas dataframe representation of the data parsed by the Drone.

        Args:
            drop_cols: [str] List of column names to drop from the dataframe before returning.
                Default: ["_id", "state_hash"]
        """
        df = DataFrame(list(self.query()))
        df = df.drop(drop_cols, axis=1)
        return df