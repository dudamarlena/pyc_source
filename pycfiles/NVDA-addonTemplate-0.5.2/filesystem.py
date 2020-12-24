# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\filesystem.py
# Compiled at: 2016-07-07 03:21:34
"""SCons.Tool.filesystem

Tool-specific initialization for the filesystem tools.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""
__revision__ = 'src/engine/SCons/Tool/filesystem.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons
from SCons.Tool.install import copyFunc
copyToBuilder, copyAsBuilder = (None, None)

def copyto_emitter(target, source, env):
    """ changes the path of the source to be under the target (which
    are assumed to be directories.
    """
    n_target = []
    for t in target:
        n_target = n_target + [ t.File(str(s)) for s in source ]

    return (n_target, source)


def copy_action_func(target, source, env):
    assert len(target) == len(source), '\ntarget: %s\nsource: %s' % (list(map(str, target)), list(map(str, source)))
    for t, s in zip(target, source):
        if copyFunc(t.get_path(), s.get_path(), env):
            return 1

    return 0


def copy_action_str(target, source, env):
    return env.subst_target_source(env['COPYSTR'], 0, target, source)


copy_action = SCons.Action.Action(copy_action_func, copy_action_str)

def generate(env):
    global copyAsBuilder
    global copyToBuilder
    try:
        env['BUILDERS']['CopyTo']
        env['BUILDERS']['CopyAs']
    except KeyError as e:
        if copyToBuilder is None:
            copyToBuilder = SCons.Builder.Builder(action=copy_action, target_factory=env.fs.Dir, source_factory=env.fs.Entry, multi=1, emitter=[
             copyto_emitter])
        if copyAsBuilder is None:
            copyAsBuilder = SCons.Builder.Builder(action=copy_action, target_factory=env.fs.Entry, source_factory=env.fs.Entry)
        env['BUILDERS']['CopyTo'] = copyToBuilder
        env['BUILDERS']['CopyAs'] = copyAsBuilder
        env['COPYSTR'] = 'Copy file(s): "$SOURCES" to "$TARGETS"'

    return


def exists(env):
    return 1