# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/t/work/cihai/cihai/cihai/constants.py
# Compiled at: 2019-08-17 05:41:51
# Size of source mod 2**32: 643 bytes
from __future__ import unicode_literals
DEFAULT_CONFIG = {'debug':False, 
 'database':{'url': 'sqlite:///{user_data_dir}/cihai.db'}, 
 'dirs':{'cache':'{user_cache_dir}', 
  'log':'{user_log_dir}', 
  'data':'{user_data_dir}'}}
UNIHAN_CONFIG = {'datasets': {'unihan': 'cihai.data.unihan.dataset.Unihan'}}