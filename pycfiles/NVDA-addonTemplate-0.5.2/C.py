# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Scanner\C.py
# Compiled at: 2016-07-07 03:21:36
"""SCons.Scanner.C

This module implements the dependency scanner for C/C++ code. 

"""
__revision__ = 'src/engine/SCons/Scanner/C.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Node.FS, SCons.Scanner, SCons.Util, SCons.cpp

class SConsCPPScanner(SCons.cpp.PreProcessor):
    """
    SCons-specific subclass of the cpp.py module's processing.

    We subclass this so that: 1) we can deal with files represented
    by Nodes, not strings; 2) we can keep track of the files that are
    missing.
    """

    def __init__(self, *args, **kw):
        SCons.cpp.PreProcessor.__init__(self, *args, **kw)
        self.missing = []

    def initialize_result(self, fname):
        self.result = SCons.Util.UniqueList([fname])

    def finalize_result(self, fname):
        return self.result[1:]

    def find_include_file(self, t):
        keyword, quote, fname = t
        result = SCons.Node.FS.find_file(fname, self.searchpath[quote])
        if not result:
            self.missing.append((fname, self.current_file))
        return result

    def read_file(self, file):
        try:
            fp = open(str(file.rfile()))
        except EnvironmentError as e:
            self.missing.append((file, self.current_file))
            return ''

        return fp.read()


def dictify_CPPDEFINES(env):
    cppdefines = env.get('CPPDEFINES', {})
    if cppdefines is None:
        return {}
    else:
        if SCons.Util.is_Sequence(cppdefines):
            result = {}
            for c in cppdefines:
                if SCons.Util.is_Sequence(c):
                    result[c[0]] = c[1]
                else:
                    result[c] = None

            return result
        if not SCons.Util.is_Dict(cppdefines):
            return {cppdefines: None}
        return cppdefines


class SConsCPPScannerWrapper(object):
    """
    The SCons wrapper around a cpp.py scanner.

    This is the actual glue between the calling conventions of generic
    SCons scanners, and the (subclass of) cpp.py class that knows how
    to look for #include lines with reasonably real C-preprocessor-like
    evaluation of #if/#ifdef/#else/#elif lines.
    """

    def __init__(self, name, variable):
        self.name = name
        self.path = SCons.Scanner.FindPathDirs(variable)

    def __call__(self, node, env, path=()):
        cpp = SConsCPPScanner(current=node.get_dir(), cpppath=path, dict=dictify_CPPDEFINES(env))
        result = cpp(node)
        for included, includer in cpp.missing:
            fmt = 'No dependency generated for file: %s (included from: %s) -- file not found'
            SCons.Warnings.warn(SCons.Warnings.DependencyWarning, fmt % (included, includer))

        return result

    def recurse_nodes(self, nodes):
        return nodes

    def select(self, node):
        return self


def CScanner():
    """Return a prototype Scanner instance for scanning source files
    that use the C pre-processor"""
    cs = SCons.Scanner.ClassicCPP('CScanner', '$CPPSUFFIXES', 'CPPPATH', '^[ \t]*#[ \t]*(?:include|import)[ \t]*(<|")([^>"]+)(>|")')
    return cs