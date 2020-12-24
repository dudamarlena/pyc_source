# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bca4abm\processors\initialize.py
# Compiled at: 2020-02-14 01:16:04
# Size of source mod 2**32: 674 bytes
import logging, os, pandas as pd, numpy as np
from activitysim.core import inject
from activitysim.core.steps.output import write_data_dictionary
from activitysim.core.steps.output import write_tables
logger = logging.getLogger(__name__)

@inject.injectable(cache=True)
def preload_injectables():
    logger.info('preload_injectables')
    inject.add_step('write_data_dictionary', write_data_dictionary)
    inject.add_step('write_tables', write_tables)