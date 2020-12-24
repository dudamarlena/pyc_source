# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/idavoll/error.py
# Compiled at: 2009-06-18 09:05:11


class Error(Exception):
    msg = ''

    def __init__(self, msg=None):
        self.msg = msg or self.msg

    def __str__(self):
        return self.msg


class NodeNotFound(Error):
    pass


class NodeExists(Error):
    pass


class NotSubscribed(Error):
    """
    Entity is not subscribed to this node.
    """
    pass


class SubscriptionExists(Error):
    """
    There already exists a subscription to this node.
    """
    pass


class Forbidden(Error):
    pass


class ItemForbidden(Error):
    pass


class ItemRequired(Error):
    pass


class NoInstantNodes(Error):
    pass


class InvalidConfigurationOption(Error):
    msg = 'Invalid configuration option'


class InvalidConfigurationValue(Error):
    msg = 'Bad configuration value'


class NodeNotPersistent(Error):
    pass


class NoRootNode(Error):
    pass


class NoCallbacks(Error):
    """
    There are no callbacks for this node.
    """
    pass


class NoCollections(Error):
    pass


class NoPublishing(Error):
    """
    This node does not support publishing.
    """
    pass