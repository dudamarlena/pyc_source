# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bca4abm\tables\persons.py
# Compiled at: 2020-02-14 01:16:04
# Size of source mod 2**32: 908 bytes
import logging, os.path, numpy as np, pandas as pd
from activitysim.core import inject
from activitysim.core import config
from bca4abm import bca4abm as bca
logger = logging.getLogger(__name__)

@inject.table()
def persons(data_dir):
    logger.debug('reading persons table')
    table_settings = config.read_model_settings('tables.yaml')
    df = bca.read_csv_table(table_name='persons', data_dir=data_dir, settings=table_settings)
    assert 'person_id' not in df.columns
    df.index = df.index + 1
    df.index.name = 'person_id'
    return df


@inject.table()
def persons_merged(persons, households):
    return inject.merge_tables(target=(persons.name), tables=[
     persons, households])