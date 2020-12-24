# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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