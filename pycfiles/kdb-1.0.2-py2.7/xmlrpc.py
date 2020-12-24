# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kdb/plugins/xmlrpc.py
# Compiled at: 2014-04-26 09:00:59
"""XML RPC

This plugin provides an XML-RPC interface to kdb
allowing other plugins to respond to "rpc" events.
"""
__version__ = '0.1'
__author__ = 'James Mills, prologic at shortcircuit dot net dot au'
from circuits.web import XMLRPC as XMLRPCDispatcher
from ..plugin import BasePlugin

class XMLRPC(BasePlugin):
    """XMLRPC Plugin

    This plugin provides no user commands. This plugin gives
    XML-RPC support to the system allowing other systems to
    interact with the system and other loaded plugins.

    The "notify" plugin is one such plugin that uses this
    to allow remote machines to send notification messages
    to a configured channel.
    """

    def init(self, *args, **kwargs):
        super(XMLRPC, self).init(*args, **kwargs)
        XMLRPCDispatcher('/xml-rpc', 'utf-8', 'rpc').register(self)