# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\mslib.py
# Compiled at: 2016-07-07 03:21:34
"""SCons.Tool.mslib

Tool-specific initialization for lib (MicroSoft library archiver).

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/mslib.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Defaults, SCons.Tool, SCons.Tool.msvs, SCons.Tool.msvc, SCons.Util
from MSCommon import msvc_exists, msvc_setup_env_once

def generate(env):
    """Add Builders and construction variables for lib to an Environment."""
    SCons.Tool.createStaticLibBuilder(env)
    msvc_setup_env_once(env)
    env['AR'] = 'lib'
    env['ARFLAGS'] = SCons.Util.CLVar('/nologo')
    env['ARCOM'] = "${TEMPFILE('$AR $ARFLAGS /OUT:$TARGET $SOURCES','$ARCOMSTR')}"
    env['LIBPREFIX'] = ''
    env['LIBSUFFIX'] = '.lib'


def exists(env):
    return msvc_exists()