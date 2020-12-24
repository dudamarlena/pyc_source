# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tox_run_before.py
# Compiled at: 2018-01-12 08:00:33
from os import system
from tox import hookimpl

@hookimpl
def tox_configure(config):
    for env in config.envlist:
        for cmd in config.envconfigs[env]._reader.getlist('run_before'):
            system(cmd)