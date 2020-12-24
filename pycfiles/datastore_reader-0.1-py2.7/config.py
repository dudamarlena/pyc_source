# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datastore_reader/utils/config.py
# Compiled at: 2011-12-20 19:24:42
import os, sys
from ConfigObject import config_module

def _init_config_obj():
    config_path = '__no_config___'
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        config_path = sys.argv[1]
    if not os.path.exists(config_path):
        config_path = 'config.ini'
    if not os.path.exists(config_path):
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.ini')
    if not os.path.exists(config_path):
        raise Exception('no config found!')
    config_module(__name__, __file__, config_path)


__initialized__ = False
if __initialized__ is False:
    _init_config_obj()
    __initialized__ = True