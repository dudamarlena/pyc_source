# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/diogo.mmartins/venvs/reloadable2.7/lib/python2.7/site-packages/reloadable/__init__.py
# Compiled at: 2018-03-06 11:04:50
from .decorators import *
from . import config

def configure(**options):
    for option, value in options.items():
        config_name = option.upper()
        if not hasattr(config, config_name):
            raise ValueError("Option '%s' doesn't exist for reloadable" % config_name)
        setattr(config, config_name, value)