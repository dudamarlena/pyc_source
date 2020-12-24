# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\tar.py
# Compiled at: 2016-07-07 03:21:34
"""SCons.Tool.tar

Tool-specific initialization for tar.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/tar.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Action, SCons.Builder, SCons.Defaults, SCons.Node.FS, SCons.Util
tars = [
 'tar', 'gtar']
TarAction = SCons.Action.Action('$TARCOM', '$TARCOMSTR')
TarBuilder = SCons.Builder.Builder(action=TarAction, source_factory=SCons.Node.FS.Entry, source_scanner=SCons.Defaults.DirScanner, suffix='$TARSUFFIX', multi=1)

def generate(env):
    """Add Builders and construction variables for tar to an Environment."""
    try:
        bld = env['BUILDERS']['Tar']
    except KeyError:
        bld = TarBuilder
        env['BUILDERS']['Tar'] = bld

    env['TAR'] = env.Detect(tars) or 'gtar'
    env['TARFLAGS'] = SCons.Util.CLVar('-c')
    env['TARCOM'] = '$TAR $TARFLAGS -f $TARGET $SOURCES'
    env['TARSUFFIX'] = '.tar'


def exists(env):
    return env.Detect(tars)