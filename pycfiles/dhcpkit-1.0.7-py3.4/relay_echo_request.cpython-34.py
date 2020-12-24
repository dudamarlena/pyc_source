# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/extensions/relay_echo_request.py
# Compiled at: 2017-06-21 07:36:34
# Size of source mod 2**32: 2731 bytes
"""
Implementation of Echo Request option handling as specified in :rfc:`4994`.
"""
from typing import List
from dhcpkit.ipv6.extensions.relay_echo_request import EchoRequestOption
from dhcpkit.ipv6.messages import RelayForwardMessage, RelayReplyMessage
from dhcpkit.ipv6.server.handlers import Handler, RelayHandler
from dhcpkit.ipv6.server.transaction_bundle import TransactionBundle

def create_cleanup_handlers() -> List[Handler]:
    """
    Create handlers to clean up stuff in the transaction bundle

    :return: Handlers to add to the handler chain
    """
    return [
     RelayEchoRequestOptionHandler()]


class RelayEchoRequestOptionHandler(RelayHandler):
    __doc__ = '\n    When a server creates a Relay-Reply, it SHOULD perform ERO processing\n    after processing the ORO and other options processing.  For each\n    option in the ERO:\n\n    a.  If the option is already in the Relay-Reply, the server MUST\n        ignore that option and continue to process any remaining options\n        in the ERO.\n\n    b.  If the option was not in the received Relay-Forward, the server\n        MUST ignore that option and continue to process any remaining\n        options in the ERO.\n\n    c.  Otherwise, the server MUST copy the option, verbatim, from the\n        received Relay-Forward to the Relay-Reply, even if the server\n        does not otherwise recognize that option.\n    '

    def handle_relay(self, bundle: TransactionBundle, relay_message_in: RelayForwardMessage, relay_message_out: RelayReplyMessage):
        """
        Handle the options for each relay message pair.

        :param bundle: The transaction bundle
        :param relay_message_in: The incoming relay message
        :param relay_message_out: Thr outgoing relay message
        """
        ero = relay_message_in.get_option_of_type(EchoRequestOption)
        if not ero:
            return
        for option_type in ero.requested_options:
            if any(option.option_type == option_type for option in relay_message_out.options):
                continue
            incoming_options = [option for option in relay_message_in.options if option.option_type == option_type]
            for option in incoming_options:
                if not relay_message_out.may_contain(option):
                    return
                relay_message_out.options.append(option)