# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/extensions/bulk_leasequery.py
# Compiled at: 2016-11-06 11:55:47
# Size of source mod 2**32: 3164 bytes
"""
Server extension to handle bulk leasequery properly
"""
import logging
from dhcpkit.ipv6.extensions.bulk_leasequery import QUERY_BY_LINK_ADDRESS, QUERY_BY_RELAY_ID, QUERY_BY_REMOTE_ID
from dhcpkit.ipv6.extensions.leasequery import LQQueryOption, LeasequeryMessage, STATUS_NOT_ALLOWED
from dhcpkit.ipv6.server.handlers import CannotRespondError, Handler, ReplyWithLeasequeryError
from dhcpkit.ipv6.server.transaction_bundle import TransactionBundle
from typing import List
logger = logging.getLogger(__name__)

def create_setup_handlers() -> List[Handler]:
    """
    Create handlers to clean up stuff in the transaction bundle

    :return: Handlers to add to the handler chain
    """
    return [
     RequireBulkLeasequeryOverTCPHandler(),
     RefuseBulkLeasequeryOverUDPHandler()]


class RequireBulkLeasequeryOverTCPHandler(Handler):
    __doc__ = '\n    A handler that makes sure only bulk leasequery is accepted over TCP.\n\n    Only LEASEQUERY, LEASEQUERY-REPLY, LEASEQUERY-DATA, and LEASEQUERY-DONE messages are allowed over the Bulk\n    Leasequery connection.  No other DHCPv6 messages are supported.  The Bulk Leasequery connection is not an\n    alternative DHCPv6 communication option for clients seeking DHCPv6 service.\n    '

    def pre(self, bundle: TransactionBundle):
        """
        Make sure that bulk leasequery options are not coming in over UDP.

        :param bundle: The transaction bundle
        """
        if not bundle.received_over_tcp:
            return
        if not isinstance(bundle.request, LeasequeryMessage):
            logger.warning('Client sent non-Leasequery message over a Bulk Leasequery socket')
            raise CannotRespondError


class RefuseBulkLeasequeryOverUDPHandler(Handler):
    __doc__ = '\n    A handler that refuses bulk leasequery over UDP.\n\n    The new queries introduced in this specification cannot be used with the UDP Leasequery protocol.  Servers that\n    implement this specification and also permit UDP queries MUST NOT accept Bulk Leasequery query-types in UDP\n    Leasequery messages.  Such servers MUST respond with an error status code of\n    :data:`~dhcpkit.ipv6.extensions.leasequery.STATUS_NOT_ALLOWED`.\n    '

    def pre(self, bundle: TransactionBundle):
        """
        Make sure that bulk leasequery options are not coming in over UDP.

        :param bundle: The transaction bundle
        """
        if bundle.received_over_tcp:
            return
        if not isinstance(bundle.request, LeasequeryMessage):
            return
        query = bundle.request.get_option_of_type(LQQueryOption)
        if query.query_type in (QUERY_BY_RELAY_ID, QUERY_BY_LINK_ADDRESS, QUERY_BY_REMOTE_ID):
            raise ReplyWithLeasequeryError(STATUS_NOT_ALLOWED, 'Query type {} is only allowed over bulk leasequery'.format(query.query_type))