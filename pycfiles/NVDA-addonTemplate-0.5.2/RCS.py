# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\RCS.py
# Compiled at: 2016-07-07 03:21:34
"""SCons.Tool.RCS.py

Tool-specific initialization for RCS.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/RCS.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Action, SCons.Builder, SCons.Util

def generate(env):
    """Add a Builder factory function and construction variables for
    RCS to an Environment."""

    def RCSFactory(env=env):
        """ """
        import SCons.Warnings as W
        W.warn(W.DeprecatedSourceCodeWarning, 'The RCS() factory is deprecated and there is no replacement.')
        act = SCons.Action.Action('$RCS_COCOM', '$RCS_COCOMSTR')
        return SCons.Builder.Builder(action=act, env=env)

    env.RCS = RCSFactory
    env['RCS'] = 'rcs'
    env['RCS_CO'] = 'co'
    env['RCS_COFLAGS'] = SCons.Util.CLVar('')
    env['RCS_COCOM'] = '$RCS_CO $RCS_COFLAGS $TARGET'


def exists(env):
    return env.Detect('rcs')