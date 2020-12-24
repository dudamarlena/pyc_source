# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/parse/headers.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
import itertools, os
from lib.core.common import checkFile
from lib.core.common import parseXmlFile
from lib.core.data import kb
from lib.core.data import paths
from lib.parse.handler import FingerprintHandler

def headersParser(headers):
    """
    This function calls a class that parses the input HTTP headers to
    fingerprint the back-end database management system operating system
    and the web application technology
    """
    if not kb.headerPaths:
        kb.headerPaths = {'cookie': os.path.join(paths.SQLMAP_XML_BANNER_PATH, 'cookie.xml'), 'microsoftsharepointteamservices': os.path.join(paths.SQLMAP_XML_BANNER_PATH, 'sharepoint.xml'), 
           'server': os.path.join(paths.SQLMAP_XML_BANNER_PATH, 'server.xml'), 
           'servlet-engine': os.path.join(paths.SQLMAP_XML_BANNER_PATH, 'servlet.xml'), 
           'set-cookie': os.path.join(paths.SQLMAP_XML_BANNER_PATH, 'cookie.xml'), 
           'x-aspnet-version': os.path.join(paths.SQLMAP_XML_BANNER_PATH, 'x-aspnet-version.xml'), 
           'x-powered-by': os.path.join(paths.SQLMAP_XML_BANNER_PATH, 'x-powered-by.xml')}
    for header in itertools.ifilter(lambda x: x in kb.headerPaths, headers):
        value = headers[header]
        xmlfile = kb.headerPaths[header]
        checkFile(xmlfile)
        handler = FingerprintHandler(value, kb.headersFp)
        parseXmlFile(xmlfile, handler)
        parseXmlFile(paths.GENERIC_XML, handler)