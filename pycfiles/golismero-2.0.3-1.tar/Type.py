# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/theHarvester/discovery/DNS/Type.py
# Compiled at: 2013-12-09 06:41:17
"""
 $Id: Type.py,v 1.6.2.1 2007/05/22 20:20:39 customdesigned Exp $

 This file is part of the pydns project.
 Homepage: http://pydns.sourceforge.net

 This code is covered by the standard Python License.

 TYPE values (section 3.2.2)
"""
A = 1
NS = 2
MD = 3
MF = 4
CNAME = 5
SOA = 6
MB = 7
MG = 8
MR = 9
NULL = 10
WKS = 11
PTR = 12
HINFO = 13
MINFO = 14
MX = 15
TXT = 16
AAAA = 28
SRV = 33
UNAME = 110
MP = 240
AXFR = 252
MAILB = 253
MAILA = 254
ANY = 255
_names = dir()
typemap = {}
for _name in _names:
    if _name[0] != '_':
        typemap[eval(_name)] = _name

def typestr(type):
    if typemap.has_key(type):
        return typemap[type]
    else:
        return `type`