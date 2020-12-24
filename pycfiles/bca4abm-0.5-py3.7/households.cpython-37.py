# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bca4abm\tables\households.py
# Compiled at: 2020-02-14 01:16:04
# Size of source mod 2**32: 1466 bytes
from builtins import range
import logging, os.path, numpy as np, pandas as pd
from activitysim.core import inject
from activitysim.core import config
from bca4abm import bca4abm as bca
logger = logging.getLogger(__name__)

@inject.table()
def households(data_dir, settings):
    logger.debug('reading households table')
    table_settings = config.read_model_settings('tables.yaml')
    base_households = bca.read_csv_table(table_name='base_households', index_col='household_id',
      data_dir=data_dir,
      settings=table_settings)
    build_households = bca.read_csv_table(table_name='build_households', index_col='household_id',
      data_dir=data_dir,
      settings=table_settings)
    households = pd.merge(base_households, build_households, left_index=True, right_index=True)
    assert 'chunk_id' not in households.columns
    households['chunk_id'] = pd.Series(list(range(len(households))), households.index)
    return households


inject.broadcast(cast='households', onto='persons',
  cast_index=True,
  onto_on='household_id')