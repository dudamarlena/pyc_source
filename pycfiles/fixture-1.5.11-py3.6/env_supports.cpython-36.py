# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/test/env_supports.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 367 bytes
"""each attribute indicates a supported module or feature."""
import os, sys

def module_exists(mod):
    try:
        __import__(mod)
    except ImportError:
        return False
    else:
        return True


sqlobject = module_exists('sqlobject')
sqlalchemy = module_exists('sqlalchemy')
elixir = module_exists('elixir')
storm = module_exists('storm')