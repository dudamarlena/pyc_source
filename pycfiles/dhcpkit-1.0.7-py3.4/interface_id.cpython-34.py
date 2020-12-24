# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/handlers/interface_id.py
# Compiled at: 2016-07-07 08:00:39
# Size of source mod 2**32: 440 bytes
"""
Option handlers for the basic :rfc:`3315` options
"""
import logging
from dhcpkit.ipv6.options import InterfaceIdOption
from dhcpkit.ipv6.server.handlers.basic_relay import CopyRelayOptionHandler
logger = logging.getLogger(__name__)

class InterfaceIdOptionHandler(CopyRelayOptionHandler):
    __doc__ = '\n    The handler for InterfaceIdOptions in relay messages\n    '

    def __init__(self):
        super().__init__(InterfaceIdOption)