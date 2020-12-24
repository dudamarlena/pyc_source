# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Scanner\Prog.py
# Compiled at: 2016-07-07 03:21:36
__revision__ = 'src/engine/SCons/Scanner/Prog.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Node, SCons.Node.FS, SCons.Scanner, SCons.Util
print_find_libs = None

def ProgramScanner(**kw):
    """Return a prototype Scanner instance for scanning executable
    files for static-lib dependencies"""
    kw['path_function'] = SCons.Scanner.FindPathDirs('LIBPATH')
    ps = SCons.Scanner.Base(scan, 'ProgramScanner', **kw)
    return ps


def _subst_libs(env, libs):
    """
    Substitute environment variables and split into list.
    """
    if SCons.Util.is_String(libs):
        libs = env.subst(libs)
        if SCons.Util.is_String(libs):
            libs = libs.split()
    elif SCons.Util.is_Sequence(libs):
        _libs = []
        for l in libs:
            _libs += _subst_libs(env, l)

        libs = _libs
    else:
        libs = [
         libs]
    return libs


def scan(node, env, libpath=()):
    """
    This scanner scans program files for static-library
    dependencies.  It will search the LIBPATH environment variable
    for libraries specified in the LIBS variable, returning any
    files it finds as dependencies.
    """
    try:
        libs = env['LIBS']
    except KeyError:
        return []

    libs = _subst_libs(env, libs)
    try:
        prefix = env['LIBPREFIXES']
        if not SCons.Util.is_List(prefix):
            prefix = [
             prefix]
    except KeyError:
        prefix = [
         '']

    try:
        suffix = env['LIBSUFFIXES']
        if not SCons.Util.is_List(suffix):
            suffix = [
             suffix]
    except KeyError:
        suffix = [
         '']

    pairs = []
    for suf in map(env.subst, suffix):
        for pref in map(env.subst, prefix):
            pairs.append((pref, suf))

    result = []
    if callable(libpath):
        libpath = libpath()
    find_file = SCons.Node.FS.find_file
    adjustixes = SCons.Util.adjustixes
    for lib in libs:
        if SCons.Util.is_String(lib):
            for pref, suf in pairs:
                l = adjustixes(lib, pref, suf)
                l = find_file(l, libpath, verbose=print_find_libs)
                if l:
                    result.append(l)

        else:
            result.append(lib)

    return result