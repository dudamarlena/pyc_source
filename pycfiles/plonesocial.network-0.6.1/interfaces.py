# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.network/plonesocial/network/interfaces.py
# Compiled at: 2013-02-27 09:25:42
from zope.interface import Interface

class INetworkGraph(Interface):
    """Stores a social network graph of users
    following/unfollowing/blocking eachother.
    """

    def set_follow(actor, other):
        """User <actor> subscribes to user <other>"""
        pass

    def set_unfollow(actor, other):
        """User <actor> unsubscribes from user <other>"""
        pass

    def get_following(actor):
        """List all users that <actor> subscribes to"""
        pass

    def get_followers(actor):
        """List all users that subscribe to <actor>"""
        pass


class INetworkTool(INetworkGraph):
    """Provide INetworkContainer as a site utility."""
    pass