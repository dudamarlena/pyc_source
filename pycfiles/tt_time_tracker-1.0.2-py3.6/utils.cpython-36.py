# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tt/dataaccess/utils.py
# Compiled at: 2020-03-21 10:42:53
# Size of source mod 2**32: 546 bytes
import os
from tt.datasources.jsondatasource import JsonStore
from tt.exceptz.exceptz import NonexistentDatasource
default_datasource_type = 'JSON'
json_default_env_var_name = 'SHEET_FILE'
json_default_db_location = '~/.tt-sheet.json'

def get_data_store(type=default_datasource_type):
    if type == 'JSON':
        return JsonStore(os.getenv(json_default_env_var_name, None) or os.path.expanduser(json_default_db_location))
    raise NonexistentDatasource('App only supports JSON datasources at the moment')