# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/WebDAV/common.py
# Compiled at: 2006-08-16 18:41:46
"""Commonly used functions for WebDAV support modules."""
__version__ = '$Revision: 1.2 $'[11:-2]
import string, time, urllib, re
from App_Common import iso8601_date, rfc850_date, rfc1123_date
from App_Common import aq_base

def absattr(attr):
    if callable(attr):
        return attr()
    return attr


def urlfix(url, s):
    n = len(s)
    if url[-n:] == s:
        url = url[:-n]
    if len(url) > 1 and url[(-1)] == '/':
        url = url[:-1]
    return url


def is_acquired(ob):
    if not hasattr(ob, 'aq_parent'):
        return 0
    if hasattr(aq_base(ob.aq_parent), absattr(ob.id)):
        return 0
    if hasattr(aq_base(ob), 'isTopLevelPrincipiaApplicationObject') and ob.isTopLevelPrincipiaApplicationObject:
        return 0
    return 1


def urlbase(url, ftype=urllib.splittype, fhost=urllib.splithost):
    if url[0] == '/':
        return url
    (type, uri) = ftype(url)
    (host, uri) = fhost(uri)
    return uri or '/'


def generateLockToken():
    return 'AA9F6414-1D77-11D3-B825-00105A989226:%.03f' % time.time()


def tokenFinder(token):
    if not token:
        return
    if token[0] == '[':
        return
    if token[0] == '<':
        token = token[1:-1]
    return token[string.find(token, ':') + 1:]


IfHdr = re.compile('(?P<resource><.+?>)?\\s*\\((?P<listitem>[^)]+)\\)')
ListItem = re.compile('(?P<not>not)?\\s*(?P<listitem><[a-zA-Z]+:[^>]*>|\\[.*?\\])', re.I)

class TagList:
    __module__ = __name__

    def __init__(self):
        self.resource = None
        self.list = []
        self.NOTTED = 0
        return


def IfParser(hdr):
    out = []
    i = 0
    while 1:
        m = IfHdr.search(hdr[i:])
        if not m:
            break
        i = i + m.end()
        tag = TagList()
        tag.resource = m.group('resource')
        if tag.resource:
            tag.resource = tag.resource[1:-1]
        listitem = m.group('listitem')
        (tag.NOTTED, tag.list) = ListParser(listitem)
        out.append(tag)

    return out


def ListParser(listitem):
    out = []
    NOTTED = 0
    i = 0
    while 1:
        m = ListItem.search(listitem[i:])
        if not m:
            break
        i = i + m.end()
        out.append(m.group('listitem'))
        if m.group('not'):
            NOTTED = 1

    return (
     NOTTED, out)