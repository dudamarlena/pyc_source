# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\CVS.py
# Compiled at: 2016-07-07 03:21:34
"""SCons.Tool.CVS.py

Tool-specific initialization for CVS.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/CVS.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Action, SCons.Builder, SCons.Util

def generate(env):
    """Add a Builder factory function and construction variables for
    CVS to an Environment."""

    def CVSFactory(repos, module='', env=env):
        """ """
        import SCons.Warnings as W
        W.warn(W.DeprecatedSourceCodeWarning, 'The CVS() factory is deprecated and there is no replacement.')
        if module != '':
            module = module + '/'
            env['CVSCOM'] = '$CVS $CVSFLAGS co $CVSCOFLAGS -d ${TARGET.dir} $CVSMODULE${TARGET.posix}'
        act = SCons.Action.Action('$CVSCOM', '$CVSCOMSTR')
        return SCons.Builder.Builder(action=act, env=env, CVSREPOSITORY=repos, CVSMODULE=module)

    env.CVS = CVSFactory
    env['CVS'] = 'cvs'
    env['CVSFLAGS'] = SCons.Util.CLVar('-d $CVSREPOSITORY')
    env['CVSCOFLAGS'] = SCons.Util.CLVar('')
    env['CVSCOM'] = '$CVS $CVSFLAGS co $CVSCOFLAGS ${TARGET.posix}'


def exists(env):
    return env.Detect('cvs')