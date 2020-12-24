# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/gwc/globals.py
# Compiled at: 2019-08-14 03:16:32
import os
from gwc import login
LOG_FILENAME = os.path.join(os.path.expanduser('~'), '.genedock/gwc/logs/gwc.log')
CONFIGFILE = os.path.join(os.path.expanduser('~'), '.genedock/gwc/configuration')
_logger = login.init_logger(LOG_FILENAME)