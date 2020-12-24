# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/theHarvester/discovery/DNS/Class.py
# Compiled at: 2013-12-09 06:41:17
"""
$Id: Class.py,v 1.6 2002/04/23 12:52:19 anthonybaxter Exp $

 This file is part of the pydns project.
 Homepage: http://pydns.sourceforge.net

 This code is covered by the standard Python License.

 CLASS values (section 3.2.4)
"""
IN = 1
CS = 2
CH = 3
HS = 4
ANY = 255
_names = dir()
classmap = {}
for _name in _names:
    if _name[0] != '_':
        classmap[eval(_name)] = _name

def classstr(klass):
    if classmap.has_key(klass):
        return classmap[klass]
    else:
        return `klass`