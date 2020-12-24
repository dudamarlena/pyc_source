# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\BitKeeper.py
# Compiled at: 2016-07-07 03:21:34
"""SCons.Tool.BitKeeper.py

Tool-specific initialization for the BitKeeper source code control
system.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/BitKeeper.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Action, SCons.Builder, SCons.Util

def generate(env):
    """Add a Builder factory function and construction variables for
    BitKeeper to an Environment."""

    def BitKeeperFactory(env=env):
        """ """
        import SCons.Warnings as W
        W.warn(W.DeprecatedSourceCodeWarning, 'The BitKeeper() factory is deprecated and there is no replacement.')
        act = SCons.Action.Action('$BITKEEPERCOM', '$BITKEEPERCOMSTR')
        return SCons.Builder.Builder(action=act, env=env)

    env.BitKeeper = BitKeeperFactory
    env['BITKEEPER'] = 'bk'
    env['BITKEEPERGET'] = '$BITKEEPER get'
    env['BITKEEPERGETFLAGS'] = SCons.Util.CLVar('')
    env['BITKEEPERCOM'] = '$BITKEEPERGET $BITKEEPERGETFLAGS $TARGET'


def exists(env):
    return env.Detect('bk')