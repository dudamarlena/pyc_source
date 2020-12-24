# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\Perforce.py
# Compiled at: 2016-07-07 03:21:35
"""SCons.Tool.Perforce.py

Tool-specific initialization for Perforce Source Code Management system.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/Perforce.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import os, SCons.Action, SCons.Builder, SCons.Node.FS, SCons.Util
_import_env = [
 'P4PORT', 'P4CLIENT', 'P4USER', 'USER', 'USERNAME', 'P4PASSWD',
 'P4CHARSET', 'P4LANGUAGE', 'SystemRoot']
PerforceAction = SCons.Action.Action('$P4COM', '$P4COMSTR')

def generate(env):
    """Add a Builder factory function and construction variables for
    Perforce to an Environment."""

    def PerforceFactory(env=env):
        """ """
        import SCons.Warnings as W
        W.warn(W.DeprecatedSourceCodeWarning, 'The Perforce() factory is deprecated and there is no replacement.')
        return SCons.Builder.Builder(action=PerforceAction, env=env)

    env.Perforce = PerforceFactory
    env['P4'] = 'p4'
    env['P4FLAGS'] = SCons.Util.CLVar('')
    env['P4COM'] = '$P4 $P4FLAGS sync $TARGET'
    try:
        environ = env['ENV']
    except KeyError:
        environ = {}
        env['ENV'] = environ

    environ['PWD'] = env.Dir('#').get_abspath()
    for var in _import_env:
        v = os.environ.get(var)
        if v:
            environ[var] = v

    if SCons.Util.can_read_reg:
        try:
            k = SCons.Util.RegOpenKeyEx(SCons.Util.hkey_mod.HKEY_LOCAL_MACHINE, 'Software\\Perforce\\environment')
            val, tok = SCons.Util.RegQueryValueEx(k, 'P4INSTROOT')
            SCons.Util.AddPathIfNotExists(environ, 'PATH', val)
        except SCons.Util.RegError:
            pass


def exists(env):
    return env.Detect('p4')