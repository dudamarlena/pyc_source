# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bca4abm\tables\benefits.py
# Compiled at: 2020-02-14 01:16:04
# Size of source mod 2**32: 1221 bytes
import logging, os.path, numpy as np, pandas as pd
from activitysim.core import inject
from activitysim.core import config
logger = logging.getLogger(__name__)

@inject.table()
def summary_results():
    logger.debug('initializing empty summary_results table')
    return pd.DataFrame(index=[0])


@inject.table()
def coc_results():
    logger.debug('initializing empty coc_results table')
    return pd.DataFrame()


@inject.injectable()
def coc_column_names():
    raise RuntimeError('coc_column_names not initialized - did you forget to run demographics_processor?')


@inject.injectable(cache=True)
def data_dictionary():
    return {}


@inject.table()
def aggregate_results():
    logger.debug('initializing empty aggregate_results table')
    return pd.DataFrame()


@inject.injectable(cache=True)
def coc_silos():
    model_settings = config.read_model_settings('aggregate_demographics.yaml')
    silos = model_settings.get('coc_silos', None)
    if silos is None:
        raise RuntimeError('coc_silos not defined in model_settings')
    return silos