# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Scanner\IDL.py
# Compiled at: 2016-07-07 03:21:36
"""SCons.Scanner.IDL

This module implements the dependency scanner for IDL (Interface
Definition Language) files.

"""
__revision__ = 'src/engine/SCons/Scanner/IDL.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Node.FS, SCons.Scanner

def IDLScan():
    """Return a prototype Scanner instance for scanning IDL source files"""
    cs = SCons.Scanner.ClassicCPP('IDLScan', '$IDLSUFFIXES', 'CPPPATH', '^[ \t]*(?:#[ \t]*include|[ \t]*import)[ \t]+(<|")([^>"]+)(>|")')
    return cs