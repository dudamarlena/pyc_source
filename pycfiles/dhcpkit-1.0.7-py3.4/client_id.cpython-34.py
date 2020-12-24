# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/handlers/client_id.py
# Compiled at: 2016-07-07 08:00:38
# Size of source mod 2**32: 399 bytes
"""
Handlers for the basic :rfc:`3315` options
"""
import logging
from dhcpkit.ipv6.options import ClientIdOption
from dhcpkit.ipv6.server.handlers.basic import CopyOptionHandler
logger = logging.getLogger(__name__)

class ClientIdHandler(CopyOptionHandler):
    __doc__ = '\n    The handler for ClientIdOptions\n    '

    def __init__(self):
        super().__init__(ClientIdOption, always_send=True)