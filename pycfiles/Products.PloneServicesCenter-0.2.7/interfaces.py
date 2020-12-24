# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/PloneRSS/content/interfaces.py
# Compiled at: 2008-10-21 05:47:01
from zope.interface import Interface

class Irss_manager(Interface):
    """Marker interface for .rss_manager.rss_manager
    """


class Irss_feed(Interface):
    """Marker interface for .rss_feed.rss_feed
    """


class Irss_item(Interface):
    """Marker interface for .rss_item.rss_item
    """


class Irss_instance(Interface):
    """Marker interface for .rss_instance.rss_instance
    """


class Irss_history(Interface):
    """Marker interface for .rss_history.rss_history
    """