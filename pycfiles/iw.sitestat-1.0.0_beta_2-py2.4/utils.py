# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/utils.py
# Compiled at: 2008-10-10 10:14:00
"""
Misc utilities
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot

def getSite():
    return getUtility(ISiteRoot)


import string

def validateSitestatName(text):
    """A Sitestat name has only ASCII chars and may contain '-' and '_'"""
    valid_letters = string.ascii_lowercase + '-_'
    if text[0] not in string.ascii_lowercase:
        return False
    if text[(-1)] not in string.ascii_lowercase:
        return False
    for char in text[1:-1]:
        if char not in valid_letters:
            return False

    return True


import unicodedata
from Products.CMFPlone.utils import getSiteEncoding
from iw.sitestat.config import BLACKLISTED_CHARS
_counterstrings_translator = string.maketrans(BLACKLISTED_CHARS, '-' * len(BLACKLISTED_CHARS))

def sitestatifyTitle(title, charset=None):
    if charset is None:
        charset = getSiteEncoding(getSite())
    utext = title.decode(charset, 'replace')
    ntext = unicodedata.normalize('NFKD', utext)
    atext = ntext.encode('ascii', 'ignore')
    atext = atext.translate(_counterstrings_translator)
    return atext


from iw.sitestat.config import PACKAGE_HOME
from Products.CMFPlone.utils import versionTupleFromString

def getFSVersionTuple():
    """Reads version.txt and returns version tuple"""
    vfile = '%s/version.txt' % PACKAGE_HOME
    v_str = open(vfile, 'r').read().lower().strip()
    return versionTupleFromString(v_str)