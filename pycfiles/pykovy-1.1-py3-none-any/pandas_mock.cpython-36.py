# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/pykovi/pandas_mock.py
# Compiled at: 2019-11-21 15:24:09
# Size of source mod 2**32: 1314 bytes
import pandas as pd, awswrangler as aw
from typing import Dict, Union, Iterable
import csv, pykovi as pk

class PandasMock(aw.Pandas):

    def __init__(self, session, custom_targets={}):
        super().__init__(session)
        self._custom_targets = custom_targets

    @property
    def custom_targets(self) -> Dict[(str, Union[(pd.DataFrame, Iterable[pd.DataFrame])])]:
        return self._custom_targets

    @custom_targets.setter
    def custom_targets(self, value: Dict[(str, Union[(pd.DataFrame, Iterable[pd.DataFrame])])]) -> None:
        self._custom_targets = value

    def read_sql_athena(self, sql, database, s3_output=None, max_result_size=None):
        custom_target = self.custom_targets.get('{0}:{1}'.format(database, sql))
        if (custom_target is not None) & (s3_output is not None):
            self._session.s3.write_dataframe(custom_target, s3_output)
        if custom_target is not None:
            return custom_target
        else:
            return super().read_sql_athena(sql,
              database, s3_output=s3_output, max_result_size=max_result_size)