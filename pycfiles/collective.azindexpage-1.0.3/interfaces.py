# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ubuntu/workspace/src/collective/awstats_hitcounter/interfaces.py
# Compiled at: 2015-10-13 16:01:11
__doc__ = 'Module where all interfaces, events and exceptions live.'
from collective.awstats_hitcounter import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from collective.awstats_hitcounter.browser.utils import blacklist
from collective.awstats_hitcounter.browser.utils import type_whitelist

class ICollectiveAwstatsHitcounterLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IRegistry(Interface):
    awstats_url_pattern = schema.Text(title=_('Awstats URL Path Pattern'), description=_('This needs to be an absolute url to your awstats system. Use {0} to represent the path query to be passed to awstats'), default=_('http://www.example.com/awstats/awstats.pl?urlfilter={0}&output=urldetail&config=www.example.com'), required=True)
    url_of_popular_page = schema.TextLine(title=_('awstats popular content page'), description=_('URL of the awstats page which shows popular content'), required=False, default='')
    prevent_direct_downloads = schema.Bool(title=_('Prevent Direct Downloads'), description=_('Prevent direct download of files'), default=True)
    view_more_item_count = schema.Int(title=_('view more item count'), description=_('Number of items to show on View More page'), default=150)
    black_list = schema.List(title=_('Blacklist'), description=_('List of items that should not be returned as popular content'), required=False, value_type=schema.TextLine(title=_('item')), default=blacklist)
    type_white_list = schema.List(title=_('Type White List'), description=_('White list of types which should be retrieved as popular content'), required=False, value_type=schema.TextLine(title=_('item')), default=type_whitelist)