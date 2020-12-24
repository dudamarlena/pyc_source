# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/theHarvester/discovery/DNS/Opcode.py
# Compiled at: 2013-12-09 06:41:17
"""
 $Id: Opcode.py,v 1.6 2002/04/23 10:51:43 anthonybaxter Exp $

 This file is part of the pydns project.
 Homepage: http://pydns.sourceforge.net

 This code is covered by the standard Python License.

 Opcode values in message header. RFC 1035, 1996, 2136.
"""
QUERY = 0
IQUERY = 1
STATUS = 2
NOTIFY = 4
UPDATE = 5
_names = dir()
opcodemap = {}
for _name in _names:
    if _name[0] != '_':
        opcodemap[eval(_name)] = _name

def opcodestr(opcode):
    if opcodemap.has_key(opcode):
        return opcodemap[opcode]
    else:
        return `opcode`