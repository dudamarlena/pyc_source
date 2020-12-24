# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Scanner\RC.py
# Compiled at: 2016-07-07 03:21:36
"""SCons.Scanner.RC

This module implements the dependency scanner for RC (Interface
Definition Language) files.

"""
__revision__ = 'src/engine/SCons/Scanner/RC.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Node.FS, SCons.Scanner, re

def RCScan():
    """Return a prototype Scanner instance for scanning RC source files"""
    res_re = '^(?:\\s*#\\s*(?:include)|.*?\\s+(?:ICON|BITMAP|CURSOR|HTML|FONT|MESSAGETABLE|TYPELIB|REGISTRY|D3DFX)\\s*.*?)\\s*(<|"| )([^>"\\s]+)(?:[>"\\s])*$'
    resScanner = SCons.Scanner.ClassicCPP('ResourceScanner', '$RCSUFFIXES', 'CPPPATH', res_re)
    return resScanner