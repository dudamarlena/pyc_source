# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/substrate/__init__.py
# Compiled at: 2012-02-03 19:38:43
from string import maketrans

def sanitize_app_id(name):
    """
    Remove unsafe characters from a app ID. Right now this just translates _ to -.
    """
    table = maketrans('_', '-')
    return name.translate(table)


from commands import *
from _version import __version__