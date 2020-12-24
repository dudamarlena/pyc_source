# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\config.py
# Compiled at: 2019-11-21 05:16:04
# Size of source mod 2**32: 1597 bytes
"""
config - configuration constants
================================================================================
"""
import os.path, appdirs

class accessError(Exception):
    pass


class parameterError(Exception):
    pass


class dbConsistencyError(Exception):
    pass


class softwareError(Exception):
    pass


CONFIGDIR = appdirs.user_data_dir('loutilities', 'Lou King')
if not os.path.exists(CONFIGDIR):
    os.makedirs(CONFIGDIR)