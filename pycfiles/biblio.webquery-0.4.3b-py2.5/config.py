# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/biblio/webquery/scripts/config.py
# Compiled at: 2009-05-06 14:40:42
"""
Constants and definitions for scripts.

"""
__docformat__ = 'restructuredtext en'
from biblio.webquery.xisbn import XisbnQuery
from biblio.webquery.loc import LocQuery
from biblio.webquery.isbndb import IsbndbQuery
try:
    from biblio.webquery import __version__
except:
    __version__ = 'unknown'

__all__ = [
 'WEBSERVICES',
 'WEBSERVICE_LOOKUP',
 'DEFAULT_WEBSERVICE']
WEBSERVICES = [
 {'id': 'xisbn', 
    'title': 'WorldCat xISBN', 
    'ctor': XisbnQuery},
 {'id': 'isbndb', 
    'title': 'ISBNdb', 
    'ctor': IsbndbQuery}]
DEFAULT_WEBSERVICE = WEBSERVICES[0]
WEBSERVICE_LOOKUP = dict([ (s['id'], s) for s in WEBSERVICES ])