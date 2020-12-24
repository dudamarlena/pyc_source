# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/request/templates.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
from lib.core.data import kb
from lib.request.connect import Connect as Request

def getPageTemplate(payload, place):
    retVal = (
     kb.originalPage, kb.errorIsNone)
    if payload and place:
        if (
         payload, place) not in kb.pageTemplates:
            page, _ = Request.queryPage(payload, place, content=True)
            kb.pageTemplates[(payload, place)] = (page, kb.lastParserStatus is None)
        retVal = kb.pageTemplates[(payload, place)]
    return retVal