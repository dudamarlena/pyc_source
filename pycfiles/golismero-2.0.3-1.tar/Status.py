# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/theHarvester/discovery/DNS/Status.py
# Compiled at: 2013-12-09 06:41:17
"""
 $Id: Status.py,v 1.7 2002/04/23 12:52:19 anthonybaxter Exp $

 This file is part of the pydns project.
 Homepage: http://pydns.sourceforge.net

 This code is covered by the standard Python License.

 Status values in message header
"""
NOERROR = 0
FORMERR = 1
SERVFAIL = 2
NXDOMAIN = 3
NOTIMP = 4
REFUSED = 5
YXDOMAIN = 6
YXRRSET = 7
NXRRSET = 8
NOTAUTH = 9
NOTZONE = 10
BADVERS = 16
BADSIG = 16
BADKEY = 17
BADTIME = 18
BADMODE = 19
BADNAME = 20
BADALG = 21
_names = dir()
statusmap = {}
for _name in _names:
    if _name[0] != '_':
        statusmap[eval(_name)] = _name

def statusstr(status):
    if statusmap.has_key(status):
        return statusmap[status]
    else:
        return `status`