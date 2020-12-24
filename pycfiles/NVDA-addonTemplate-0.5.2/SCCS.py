# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\SCCS.py
# Compiled at: 2016-07-07 03:21:34
"""SCons.Tool.SCCS.py

Tool-specific initialization for SCCS.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/SCCS.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Action, SCons.Builder, SCons.Util

def generate(env):
    """Add a Builder factory function and construction variables for
    SCCS to an Environment."""

    def SCCSFactory(env=env):
        """ """
        import SCons.Warnings as W
        W.warn(W.DeprecatedSourceCodeWarning, 'The SCCS() factory is deprecated and there is no replacement.')
        act = SCons.Action.Action('$SCCSCOM', '$SCCSCOMSTR')
        return SCons.Builder.Builder(action=act, env=env)

    env.SCCS = SCCSFactory
    env['SCCS'] = 'sccs'
    env['SCCSFLAGS'] = SCons.Util.CLVar('')
    env['SCCSGETFLAGS'] = SCons.Util.CLVar('')
    env['SCCSCOM'] = '$SCCS $SCCSFLAGS get $SCCSGETFLAGS $TARGET'


def exists(env):
    return env.Detect('sccs')