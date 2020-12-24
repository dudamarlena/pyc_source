# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/PloneRSS/content/interfaces.py
# Compiled at: 2008-10-21 05:47:01
from zope.interface import Interface

class Irss_manager(Interface):
    """Marker interface for .rss_manager.rss_manager
    """
    pass


class Irss_feed(Interface):
    """Marker interface for .rss_feed.rss_feed
    """
    pass


class Irss_item(Interface):
    """Marker interface for .rss_item.rss_item
    """
    pass


class Irss_instance(Interface):
    """Marker interface for .rss_instance.rss_instance
    """
    pass


class Irss_history(Interface):
    """Marker interface for .rss_history.rss_history
    """
    pass