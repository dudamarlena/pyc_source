# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\default.py
# Compiled at: 2016-07-07 03:21:33
"""SCons.Tool.default

Initialization with a default tool list.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/default.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Tool

def generate(env):
    """Add default tools."""
    for t in SCons.Tool.tool_list(env['PLATFORM'], env):
        SCons.Tool.Tool(t)(env)


def exists(env):
    return 1