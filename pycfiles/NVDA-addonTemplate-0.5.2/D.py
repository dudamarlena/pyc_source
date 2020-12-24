# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Scanner\D.py
# Compiled at: 2016-07-07 03:21:36
"""SCons.Scanner.D

Scanner for the Digital Mars "D" programming language.

Coded by Andy Friesen
17 Nov 2003

"""
__revision__ = 'src/engine/SCons/Scanner/D.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import re, SCons.Scanner

def DScanner():
    """Return a prototype Scanner instance for scanning D source files"""
    ds = D()
    return ds


class D(SCons.Scanner.Classic):

    def __init__(self):
        SCons.Scanner.Classic.__init__(self, name='DScanner', suffixes='$DSUFFIXES', path_variable='DPATH', regex='import\\s+(?:[a-zA-Z0-9_.]+)\\s*(?:,\\s*(?:[a-zA-Z0-9_.]+)\\s*)*;')
        self.cre2 = re.compile('(?:import\\s)?\\s*([a-zA-Z0-9_.]+)\\s*(?:,|;)', re.M)

    def find_include(self, include, source_dir, path):
        inc = include.replace('.', '/')
        i = SCons.Node.FS.find_file(inc + '.d', (source_dir,) + path)
        if i is None:
            i = SCons.Node.FS.find_file(inc + '.di', (source_dir,) + path)
        return (
         i, include)

    def find_include_names(self, node):
        includes = []
        for i in self.cre.findall(node.get_text_contents()):
            includes = includes + self.cre2.findall(i)

        return includes