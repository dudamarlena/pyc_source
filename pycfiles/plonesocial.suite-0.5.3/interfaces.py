# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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