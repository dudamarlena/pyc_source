# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/transaction_bundle.py
# Compiled at: 2017-06-08 10:49:31
# Size of source mod 2**32: 12264 bytes
"""
An object to hold everything related to a request/response transaction
"""
import codecs, logging
from ipaddress import IPv6Address
from typing import Iterable, Iterator, List, Optional, Tuple, Type, TypeVar
from dhcpkit.ipv6.messages import ClientServerMessage, Message, RelayReplyMessage
from dhcpkit.ipv6.options import ClientIdOption, Option
from dhcpkit.ipv6.utils import split_relay_chain
logger = logging.getLogger(__name__)
SomeOption = TypeVar('SomeOption', bound='Option')

class TransactionBundle:
    __doc__ = '\n    A bundle with all data about a transaction. This makes it much easier to pass around multiple pieces of information.\n\n    :type incoming_message: Message\n    :type received_over_multicast: bool\n    :type request: ClientServerMessage\n    :type incoming_relay_messages: List[RelayForwardMessage]\n    :type responses: MessagesList\n    :type outgoing_relay_messages: Optional[List[RelayReplyMessage]]\n    :type handled_options: List[Option]\n    :type marks: Set[str]\n    :type handler_data: Dict[Handler, object]\n    '

    def __init__(self, incoming_message: Message, received_over_multicast: bool, received_over_tcp: bool=False,
                 allow_rapid_commit: bool=False,
                 marks: Iterable[str]=None):
        self.incoming_message = incoming_message
        self.received_over_multicast = received_over_multicast
        self.received_over_tcp = received_over_tcp
        self.allow_unicast = False
        self.allow_rapid_commit = allow_rapid_commit
        self.request = None
        self.incoming_relay_messages = []
        self.request, self.incoming_relay_messages = split_relay_chain(incoming_message)
        if self.received_over_tcp:
            if len(self.incoming_relay_messages) > 1:
                raise ValueError('Relayed message on TCP connection, ignoring')
        self.responses = MessagesList()
        self.outgoing_relay_messages = None
        self.handled_options = []
        self.marks = set(marks or [])
        self.handler_data = {}

    def __str__(self) -> str:
        client_id = self.request.get_option_of_type(ClientIdOption)
        if client_id:
            duid = codecs.encode(client_id.duid.save(), 'hex').decode('ascii')
        else:
            duid = 'unknown'
        output = '{} from {}'.format(type(self.request).__name__, duid)
        if self.received_over_tcp:
            output += ' over TCP'
        if self.incoming_relay_messages:
            link_address = self.incoming_relay_messages[0].link_address
            link_name = str(link_address) if not link_address.is_unspecified else 'LDRA'
            output += ' at {} via {}'.format(self.incoming_relay_messages[0].peer_address, link_name)
            for relay in self.incoming_relay_messages[1:]:
                link_name = str(relay.link_address) if not relay.link_address.is_unspecified else 'LDRA'
                output += ' -> {}'.format(link_name)

        if self.marks:
            output += " with marks '{}'".format("', '".join(self.marks))
        return output

    @property
    def response(self):
        """
        Backwards-compatibility handling for when we only supported one response. TCP connections can support more than
        one response, but for normal DHCPv6 a single response is all we need is a single one, so make this use-case
        easy and backwards-compatible.

        :return: The first response
        """
        if not self.responses:
            return
        return self.responses[0]

    @response.setter
    def response(self, new_response: ClientServerMessage):
        """
        Backwards-compatibility handling for when we only supported one response. TCP connections can support more than
        one response, but for normal DHCPv6 a single response is all we need is a single one, so make this use-case
        easy and backwards-compatible.

        :param new_response: The new response
        """
        if new_response is None:
            self.responses = MessagesList()
        else:
            if self.responses:
                self.responses[0] = new_response
            else:
                self.responses = MessagesList(new_response)

    def mark_handled(self, option: Option):
        """
        Mark the given option as handled. Not all options are specifically handled. This is mostly useful for
        options like IANAOption, IATAOption and IAPDOption.

        :param option: The option to mark as handled
        """
        if option not in self.handled_options:
            self.handled_options.append(option)

    def get_unhandled_options(self, option_types: Type[SomeOption] or Tuple[Type[SomeOption]]) -> List[SomeOption]:
        """
        Get a list of all Options in the request that haven't been marked as handled

        :return: The list of unanswered Options
        """
        return [option for option in self.request.options if isinstance(option, option_types) and option not in self.handled_options]

    def add_mark(self, mark: str):
        """
        Add this mark to the set.

        :param mark: The mark to add
        """
        self.marks.add(mark.strip())

    @property
    def link_address(self) -> IPv6Address:
        """
        Find the link address that identifies where this request is coming from. For TCP connections we use the remote
        endpoint of the connection instead.
        """
        if self.received_over_tcp:
            return self.incoming_relay_messages[(-1)].peer_address
        for relay in self.incoming_relay_messages:
            if not relay.link_address.is_unspecified and not relay.link_address.is_loopback and not relay.link_address.is_link_local:
                return relay.link_address

        return IPv6Address('::')

    @property
    def relays(self) -> List[IPv6Address]:
        """
        Get a list of all the relays that this message went through
        """
        return [relay.link_address for relay in self.incoming_relay_messages if not relay.link_address.is_unspecified]

    def create_outgoing_relay_messages(self):
        """
        Create a plain chain of RelayReplyMessages for the current response
        """
        self.outgoing_relay_messages = []
        if not self.incoming_relay_messages:
            return
        outgoing_message = self.incoming_relay_messages[(-1)].wrap_response(self.response)
        self.outgoing_relay_messages = []
        while isinstance(outgoing_message, RelayReplyMessage):
            self.outgoing_relay_messages.insert(0, outgoing_message)
            outgoing_message = outgoing_message.relayed_message

    @property
    def outgoing_message(self) -> Optional[RelayReplyMessage]:
        """
        Wrap the response in a relay chain if necessary. Only works when there is a single response.
        """
        if self.response is None:
            return
        else:
            messages = list(self.outgoing_messages)
            if not messages:
                return
            return messages[0]

    @property
    def outgoing_messages(self) -> Iterable[RelayReplyMessage]:
        """
        Wrap the responses in a relay chain if necessary and iterate over them.

        .. warning::
            Be careful when iterating over outgoing messages. When iterating over multiple responses the original relay
            messages will be updated to contain the next response when proceeding the the next one!
        """
        if self.incoming_relay_messages:
            if not self.outgoing_relay_messages:
                self.create_outgoing_relay_messages()
        for response in self.responses:
            if not response.from_server_to_client:
                logger.error('A server should not send {} to a client'.format(response.__class__.__name__))
                continue
            if self.outgoing_relay_messages:
                self.outgoing_relay_messages[0].relayed_message = response
                yield self.outgoing_relay_messages[(-1)]
            else:
                yield response


class MessagesList:
    __doc__ = '\n    A weird iterator wrapper. This allows handlers to manipulate the first message while not needing to load all of the\n    subsequent messages in memory.\n    '

    def __init__(self, first_message: ClientServerMessage=None,
                 subsequent_messages: Iterator[ClientServerMessage]=None):
        self.first_message = first_message
        self.subsequent_messages = subsequent_messages or iter([])
        self.has_been_iterated_over = False

    def __iter__(self) -> Iterator[ClientServerMessage]:
        """
        An iterator for our messages.

        :return: The messages
        """
        if not self.first_message:
            return
        yield self.first_message
        yield from self.subsequent_messages

    def __getitem__(self, index: int) -> ClientServerMessage:
        """
        We are asked for a specific index, we only support 0.

        :param index: Index of the requested message
        :return: The requested message
        """
        if index != 0:
            raise IndexError('MessagesList only supports directly accessing the first message directly')
        if self.first_message:
            return self.first_message
        raise IndexError

    def __setitem__(self, index: int, new_message: ClientServerMessage):
        """
        Overwrite the first message (we only support index 0).

        :param index: The index of the message to be overwritten
        :param new_message: The new message
        """
        if index != 0:
            raise IndexError('MessagesList only supports directly accessing the first message directly')
        self.first_message = new_message

    def __bool__(self):
        """
        Return whether there are messages, i.e. there is at least a first message.

        :return: Whether we have messages
        """
        return bool(self.first_message)