# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/myams/interfaces/search.py
# Compiled at: 2014-05-15 04:23:22
from zope.interface import Interface
from zope.schema import TextLine
from ztfy.myams import _

class IMyAMSApplicationSearch(Interface):
    """MyAMS application search configuration interface"""
    site_search_placeholder = TextLine(title=_('Site search placeholder'), required=False, default=_('Search...'))
    site_search_handler = TextLine(title=_('Site search handler'), required=False, default='#search.html')
    mobile_search_placeholder = TextLine(title=_('Mobile search placeholder'), required=False, default=_('Search...'))
    mobile_search_handler = TextLine(title=_('Mobile search handler'), required=False, default='#search.html')