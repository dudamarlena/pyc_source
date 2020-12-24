# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/io/genomicfile.py
# Compiled at: 2019-09-04 14:12:25
# Size of source mod 2**32: 1815 bytes
import modin.pandas as pd

class GenomicFile(object):
    dataframe_lib = pd

    @classmethod
    def read(cls, *args, **kwargs):
        df = (cls._read)(*args, **kwargs)
        df._mango_parse = cls._parse(df)
        df._mango_to_json = cls._to_json(df)
        df._pileup_visualization = cls._visualization(df)
        return df

    @classmethod
    def _read(cls, *args, **kwargs):
        raise NotImplementedError('Must be implemented in children classes')

    @classmethod
    def _parse(cls, df):
        raise NotImplementedError('Must be implemented in children classes')

    @classmethod
    def _to_json(cls, df):
        raise NotImplementedError('Must be implemented in children classes')

    @classmethod
    def _visualization(cls, df):
        raise NotImplementedError('Must be implemented in children classes')

    @classmethod
    def from_pandas(cls, df):
        df._mango_parse = cls._parse(df)
        df._mango_to_json = cls._to_json(df)
        return df