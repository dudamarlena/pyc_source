# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\jar.py
# Compiled at: 2016-07-07 03:21:34
"""SCons.Tool.jar

Tool-specific initialization for jar.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/jar.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Subst, SCons.Util

def jarSources(target, source, env, for_signature):
    """Only include sources that are not a manifest file."""
    try:
        env['JARCHDIR']
    except KeyError:
        jarchdir_set = False

    jarchdir_set = True
    jarchdir = env.subst('$JARCHDIR', target=target, source=source)
    if jarchdir:
        jarchdir = env.fs.Dir(jarchdir)
    result = []
    for src in source:
        contents = src.get_text_contents()
        if contents[:16] != 'Manifest-Version':
            if jarchdir_set:
                _chdir = jarchdir
            else:
                try:
                    _chdir = src.attributes.java_classdir
                except AttributeError:
                    _chdir = None

            if _chdir:
                src = SCons.Subst.Literal(src.get_path(_chdir))
                result.append('-C')
                result.append(_chdir)
            result.append(src)

    return result


def jarManifest(target, source, env, for_signature):
    """Look in sources for a manifest file, if any."""
    for src in source:
        contents = src.get_text_contents()
        if contents[:16] == 'Manifest-Version':
            return src

    return ''


def jarFlags(target, source, env, for_signature):
    """If we have a manifest, make sure that the 'm'
    flag is specified."""
    jarflags = env.subst('$JARFLAGS', target=target, source=source)
    for src in source:
        contents = src.get_text_contents()
        if contents[:16] == 'Manifest-Version':
            if 'm' not in jarflags:
                return jarflags + 'm'
            break

    return jarflags


def generate(env):
    """Add Builders and construction variables for jar to an Environment."""
    SCons.Tool.CreateJarBuilder(env)
    env['JAR'] = 'jar'
    env['JARFLAGS'] = SCons.Util.CLVar('cf')
    env['_JARFLAGS'] = jarFlags
    env['_JARMANIFEST'] = jarManifest
    env['_JARSOURCES'] = jarSources
    env['_JARCOM'] = '$JAR $_JARFLAGS $TARGET $_JARMANIFEST $_JARSOURCES'
    env['JARCOM'] = "${TEMPFILE('$_JARCOM','$JARCOMSTR')}"
    env['JARSUFFIX'] = '.jar'


def exists(env):
    return 1