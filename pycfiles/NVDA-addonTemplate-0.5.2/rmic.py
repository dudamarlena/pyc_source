# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\rmic.py
# Compiled at: 2016-07-07 03:21:35
"""SCons.Tool.rmic

Tool-specific initialization for rmic.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/rmic.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import os.path, SCons.Action, SCons.Builder, SCons.Node.FS, SCons.Util

def emit_rmic_classes(target, source, env):
    """Create and return lists of Java RMI stub and skeleton
    class files to be created from a set of class files.
    """
    class_suffix = env.get('JAVACLASSSUFFIX', '.class')
    classdir = env.get('JAVACLASSDIR')
    if not classdir:
        try:
            s = source[0]
        except IndexError:
            classdir = '.'
        else:
            try:
                classdir = s.attributes.java_classdir
            except AttributeError:
                classdir = '.'

    classdir = env.Dir(classdir).rdir()
    if str(classdir) == '.':
        c_ = None
    else:
        c_ = str(classdir) + os.sep
    slist = []
    for src in source:
        try:
            classname = src.attributes.java_classname
        except AttributeError:
            classname = str(src)
            if c_ and classname[:len(c_)] == c_:
                classname = classname[len(c_):]
            if class_suffix and classname[:-len(class_suffix)] == class_suffix:
                classname = classname[-len(class_suffix):]

        s = src.rfile()
        s.attributes.java_classdir = classdir
        s.attributes.java_classname = classname
        slist.append(s)

    stub_suffixes = ['_Stub']
    if env.get('JAVAVERSION') == '1.4':
        stub_suffixes.append('_Skel')
    tlist = []
    for s in source:
        for suff in stub_suffixes:
            fname = s.attributes.java_classname.replace('.', os.sep) + suff + class_suffix
            t = target[0].File(fname)
            t.attributes.java_lookupdir = target[0]
            tlist.append(t)

    return (
     tlist, source)


RMICAction = SCons.Action.Action('$RMICCOM', '$RMICCOMSTR')
RMICBuilder = SCons.Builder.Builder(action=RMICAction, emitter=emit_rmic_classes, src_suffix='$JAVACLASSSUFFIX', target_factory=SCons.Node.FS.Dir, source_factory=SCons.Node.FS.File)

def generate(env):
    """Add Builders and construction variables for rmic to an Environment."""
    env['BUILDERS']['RMIC'] = RMICBuilder
    env['RMIC'] = 'rmic'
    env['RMICFLAGS'] = SCons.Util.CLVar('')
    env['RMICCOM'] = '$RMIC $RMICFLAGS -d ${TARGET.attributes.java_lookupdir} -classpath ${SOURCE.attributes.java_classdir} ${SOURCES.attributes.java_classname}'
    env['JAVACLASSSUFFIX'] = '.class'


def exists(env):
    return 1