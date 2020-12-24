# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/extensions/leasequery.py
# Compiled at: 2017-06-08 11:09:29
# Size of source mod 2**32: 28466 bytes
"""
Implementation of the Leasequery protocol extension as specified in :rfc:`5007`.
"""
from ipaddress import IPv6Address
from struct import pack, unpack_from
from typing import Iterable, List, Optional, Type, TypeVar, Union
from dhcpkit.display_strings import lq_query_types
from dhcpkit.ipv6.messages import ClientServerMessage, Message, RelayForwardMessage
from dhcpkit.ipv6.options import ClientIdOption, IAAddressOption, Option, OptionRequestOption, ServerIdOption, StatusCodeOption
from dhcpkit.protocol_element import ElementDataRepresentation
MSG_LEASEQUERY = 14
MSG_LEASEQUERY_REPLY = 15
QUERY_BY_ADDRESS = 1
QUERY_BY_CLIENT_ID = 2
OPTION_LQ_QUERY = 44
OPTION_CLIENT_DATA = 45
OPTION_CLT_TIME = 46
OPTION_LQ_RELAY_DATA = 47
OPTION_LQ_CLIENT_LINK = 48
STATUS_UNKNOWN_QUERY_TYPE = 7
STATUS_MALFORMED_QUERY = 8
STATUS_NOT_CONFIGURED = 9
STATUS_NOT_ALLOWED = 10
SomeOption = TypeVar('SomeOption', bound='Option')

class LeasequeryMessage(ClientServerMessage):
    __doc__ = "\n    The LEASEQUERY and LEASEQUERY-REPLY messages use the Client/Server message formats. A requestor sends a LEASEQUERY\n    message to any available server to obtain information on a client's leases.  The options in an OPTION_LQ_QUERY\n    determine the query.\n    "
    message_type = MSG_LEASEQUERY
    from_client_to_server = True


class LeasequeryReplyMessage(ClientServerMessage):
    __doc__ = '\n    The LEASEQUERY and LEASEQUERY-REPLY messages use the Client/Server message formats. A server sends a\n    LEASEQUERY-REPLY message containing client data in response to a LEASEQUERY message.\n    '
    message_type = MSG_LEASEQUERY_REPLY
    from_server_to_client = True


class LQQueryOption(Option):
    __doc__ = "\n    :rfc:`5007#section-4.1.2.1`\n\n    The Query option is used only in a LEASEQUERY message and identifies\n    the query being performed.  The option includes the query type, link-\n    address (or 0::0), and option(s) to provide data needed for the\n    query.\n\n    The format of the Query option is shown below:\n\n    .. code-block:: none\n\n        0                   1                   2                   3\n        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n       |        OPTION_LQ_QUERY        |         option-len            |\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n       |   query-type  |                                               |\n       +-+-+-+-+-+-+-+-+                                               |\n       |                                                               |\n       |                         link-address                          |\n       |                                                               |\n       |               +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n       |               |                                               .\n       +-+-+-+-+-+-+-+-+                                               .\n       .                         query-options                         .\n       .                                                               .\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    option-code\n        OPTION_LQ_QUERY (44)\n\n    option-len\n        17 + length of query-options field.\n\n    link-address\n        A global address that will be used by the\n        server to identify the link to which the\n        query applies, or 0::0 if unspecified.\n\n    query-type\n        The query requested (see below).\n\n    query-options\n        The options related to the query.\n\n    The query-type and required query-options are:\n\n    QUERY_BY_ADDRESS (1)\n        The query-options MUST contain an\n        OPTION_IAADDR option [2].  The link-address field, if not 0::0,\n        specifies an address for the link on which the client is located\n        if the address in the OPTION_IAADDR option is of insufficient\n        scope.  Only the information for the client that has a lease for\n        the specified address or was delegated a prefix that contains the\n        specified address is returned (if available).\n\n    QUERY_BY_CLIENTID (2)\n        The query-options MUST contain an\n        OPTION_CLIENTID option [2].  The link-address field, if not 0::0,\n        specifies an address for the link on which the client is located.\n        If the link-address field is 0::0, the server SHOULD search all of\n        its links for the client.\n\n    The query-options MAY also include an OPTION_ORO option [2] to\n    indicate the options for each client that the requestor would like\n    the server to return.  Note that this OPTION_ORO is distinct and\n    separate from an OPTION_ORO that may be in the requestor's LEASEQUERY\n    message.\n\n    If a server receives an OPTION_LQ_QUERY with a query-type it does not\n    support, the server SHOULD return an UnknownQueryType status-code.\n    If a server receives a supported query-type but the query-options is\n    missing a required option, the server SHOULD return a MalformedQuery\n    status-code.\n\n    This checking of mandatory options is done in the server code, not in\n    :meth:`~LQQueryOption.validate()`.\n\n    :type query_type: int\n    :type link_address: IPv6Address\n    :type options: List[Option]\n    "
    option_type = OPTION_LQ_QUERY

    def __init__(self, query_type: int=0,
                 link_address: IPv6Address=None, options: Iterable[Option]=None):
        self.query_type = query_type
        self.link_address = link_address or IPv6Address('::')
        self.options = list(options or [])

    def display_query_type(self) -> ElementDataRepresentation:
        """
        Nicer representation of query types
        :return: Representation of query type
        """
        display = lq_query_types.get(self.query_type, 'Unknown')
        return ElementDataRepresentation('{} ({})'.format(display, self.query_type))

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.query_type, int) or not 0 <= self.query_type < 256:
            raise ValueError('Query-type must be an unsigned 8 bit integer')
        if not isinstance(self.link_address, IPv6Address) or self.link_address.is_loopback or self.link_address.is_multicast:
            raise ValueError('Link address must be a valid IPv6 address')
        self.validate_contains(self.options)
        for option in self.options:
            option.validate()

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset, option_len = self.parse_option_header(buffer, offset, length, min_length=17)
        header_offset = my_offset
        self.query_type = buffer[(offset + my_offset)]
        my_offset += 1
        self.link_address = IPv6Address(buffer[offset + my_offset:offset + my_offset + 16])
        my_offset += 16
        self.options = []
        max_offset = option_len + header_offset
        while max_offset > my_offset:
            used_buffer, option = Option.parse(buffer, offset=offset + my_offset)
            self.options.append(option)
            my_offset += used_buffer

        if my_offset != max_offset:
            raise ValueError('Option length does not match the combined length of the parsed options')
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        options_buffer = bytearray()
        for option in self.options:
            options_buffer.extend(option.save())

        buffer = bytearray()
        buffer.extend(pack('!HHB', self.option_type, len(options_buffer) + 17, self.query_type))
        buffer.extend(self.link_address.packed)
        buffer.extend(options_buffer)
        return buffer

    def get_options_of_type(self, *args: Type[SomeOption]) -> List[SomeOption]:
        """
        Get all options that are subclasses of the given class.

        :param args: The classes to look for
        :returns: The list of options
        """
        classes = tuple(args)
        return [option for option in self.options if isinstance(option, classes)]

    def get_option_of_type(self, *args: Type[SomeOption]) -> Optional[SomeOption]:
        """
        Get the first option that is a subclass of the given class.

        :param args: The classes to look for
        :returns: The option or None
        """
        classes = tuple(args)
        for option in self.options:
            if isinstance(option, classes):
                return option


class ClientDataOption(Option):
    __doc__ = "\n    :rfc:`5007#section-4.1.2.2`\n\n    The Client Data option is used to encapsulate the data for a single\n    client on a single link in a LEASEQUERY-REPLY message.\n\n    The format of the Client Data option is shown below:\n\n    .. code-block:: none\n\n        0                   1                   2                   3\n        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n       |       OPTION_CLIENT_DATA      |         option-len            |\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n       .                                                               .\n       .                        client-options                         .\n       .                                                               .\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    option-code\n        OPTION_CLIENT_DATA (45)\n\n    option-len\n        Length, in octets, of the encapsulated client-options field.\n\n    client-options\n        The options associated with this client.\n\n    The encapsulated client-options include the OPTION_CLIENTID,\n    OPTION_IAADDR, OPTION_IAPREFIX, and OPTION_CLT_TIME options and other\n    options specific to the client and requested by the requestor in the\n    OPTION_ORO in the OPTION_LQ_QUERY's query-options.  The server MUST\n    return all of the client's statefully assigned addresses and\n    delegated prefixes, with a non-zero valid lifetime, on the link.\n\n    :type options: List[Option]\n    "
    option_type = OPTION_CLIENT_DATA

    def __init__(self, options: Iterable[Option]=None):
        self.options = list(options or [])

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        self.validate_contains(self.options)
        for option in self.options:
            option.validate()

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset, option_len = self.parse_option_header(buffer, offset, length, min_length=0)
        header_offset = my_offset
        self.options = []
        max_offset = option_len + header_offset
        while max_offset > my_offset:
            used_buffer, option = Option.parse(buffer, offset=offset + my_offset)
            self.options.append(option)
            my_offset += used_buffer

        if my_offset != max_offset:
            raise ValueError('Option length does not match the combined length of the parsed options')
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        options_buffer = bytearray()
        for option in self.options:
            options_buffer.extend(option.save())

        buffer = bytearray()
        buffer.extend(pack('!HH', self.option_type, len(options_buffer)))
        buffer.extend(options_buffer)
        return buffer

    def get_options_of_type(self, *args: Type[SomeOption]) -> List[SomeOption]:
        """
        Get all options that are subclasses of the given class.

        :param args: The classes to look for
        :returns: The list of options
        """
        classes = tuple(args)
        return [option for option in self.options if isinstance(option, classes)]

    def get_option_of_type(self, *args: Type[SomeOption]) -> Optional[SomeOption]:
        """
        Get the first option that is a subclass of the given class.

        :param args: The classes to look for
        :returns: The option or None
        """
        classes = tuple(args)
        for option in self.options:
            if isinstance(option, classes):
                return option


class CLTTimeOption(Option):
    __doc__ = '\n    :rfc:`5007#section-4.1.2.3`\n\n    The Client Last Transaction Time option is encapsulated in an\n    OPTION_CLIENT_DATA and identifies how long ago the server last\n    communicated with the client, in seconds.\n\n    The format of the Client Last Transaction Time option is shown below:\n\n    .. code-block:: none\n\n        0                   1                   2                   3\n        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n       |        OPTION_CLT_TIME        |         option-len            |\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n       |                 client-last-transaction-time                  |\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    option-code\n        OPTION_CLT_TIME (46)\n\n    option-len\n        4\n\n    client-last-transaction-time\n        The number of seconds since the server last\n        communicated with the client (on that link).\n\n    The client-last-transaction-time is a positive value and reflects the\n    number of seconds since the server last communicated with the client\n    (on that link).\n\n    :type clt_time: int\n    '
    option_type = OPTION_CLT_TIME

    def __init__(self, clt_time: int=0):
        self.clt_time = clt_time

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.clt_time, int) or not 0 <= self.clt_time < 4294967296:
            raise ValueError('CLT time must be an unsigned 32 bit integer')

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset, option_len = self.parse_option_header(buffer, offset, length, min_length=4, max_length=4)
        self.clt_time = unpack_from('!I', buffer, offset=offset + my_offset)[0]
        my_offset += 4
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        buffer = bytearray()
        buffer.extend(pack('!HHI', self.option_type, 4, self.clt_time))
        return buffer


class LQRelayDataOption(Option):
    __doc__ = "\n    :rfc:`5007#section-4.1.2.4`\n\n    The Relay Data option is used only in a LEASEQUERY-REPLY message and\n    provides the relay agent information used when the client last\n    communicated with the server.\n\n    The format of the Relay Data option is shown below:\n\n    .. code-block:: none\n\n        0                   1                   2                   3\n        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n       |     OPTION_LQ_RELAY_DATA      |         option-len            |\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n       |                                                               |\n       |                  peer-address (IPv6 address)                  |\n       |                                                               |\n       |                                                               |\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n       |                                                               |\n       |                       DHCP-relay-message                      |\n       .                                                               .\n       .                                                               .\n       .                                                               .\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    option-code\n        OPTION_LQ_RELAY_DATA (47)\n\n    option-len\n        16 + length of DHCP-relay-message.\n\n    peer-address\n        The address of the relay agent from which\n        the relayed message was received by the\n        server.\n\n    DHCP-relay-message\n        The last complete relayed message, excluding\n        the client's message OPTION_RELAY_MSG,\n        received by the server.\n\n    This option is used by the server to return full relay agent\n    information for a client.  It MUST NOT be returned if the server does\n    not have such information, either because the client communicated\n    directly (without relay agent) with the server or if the server did\n    not retain such information.\n\n    If returned, the DHCP-relay-message MUST contain a valid (perhaps\n    multi-hop) RELAY-FORW message as the most recently received by the\n    server for the client.  However, the (innermost) OPTION_RELAY_MSG\n    option containing the client's message MUST have been removed.\n\n    This option SHOULD only be returned if requested by the OPTION_ORO of\n    the OPTION_LQ_QUERY.\n\n    :type peer_address: IPv6Address\n    :type relay_message: RelayForwardMessage\n    "
    option_type = OPTION_LQ_RELAY_DATA

    def __init__(self, peer_address: IPv6Address=None,
                 relay_message: RelayForwardMessage=None):
        self.peer_address = peer_address
        self.relay_message = relay_message or RelayForwardMessage

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.peer_address, IPv6Address) or self.peer_address.is_loopback or self.peer_address.is_multicast or self.peer_address.is_unspecified:
            raise ValueError('Peer address must be a valid IPv6 address')
        if not isinstance(self.relay_message, Message):
            raise ValueError('Relay message must be an IPv6 DHCP message')
        if not self.may_contain(self.relay_message):
            raise ValueError('{} cannot contain {}'.format(self.__class__.__name__, self.relay_message.__class__.__name__))
        self.relay_message.validate()

    def load_from(self, buffer: bytes, offset: int=0,
                  length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset, option_len = self.parse_option_header(buffer, offset, length, min_length=20)
        self.peer_address = IPv6Address(buffer[offset + my_offset:offset + my_offset + 16])
        my_offset += 16
        message_len, self.relay_message = Message.parse(buffer, offset=offset + my_offset, length=option_len - 16)
        my_offset += message_len
        if message_len != option_len - 16:
            raise ValueError('The embedded message has a different length than the Relay Data Option')
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        message = self.relay_message.save()
        buffer = bytearray()
        buffer.extend(pack('!HH', self.option_type, len(message) + 16))
        buffer.extend(self.peer_address.packed)
        buffer.extend(message)
        return buffer


class LQClientLink(Option):
    __doc__ = "\n    :rfc:`5007#section-4.1.2.5`\n\n    The Client Link option is used only in a LEASEQUERY-REPLY message and\n    identifies the links on which the client has one or more bindings.\n    It is used in reply to a query when no link-address was specified and\n    the client is found to be on more than one link.\n\n    The format of the Client Link option is shown below:\n\n    .. code-block:: none\n\n        0                   1                   2                   3\n        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n       |     OPTION_LQ_CLIENT_LINK     |         option-len            |\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n       |                                                               |\n       |                  link-address (IPv6 address)                  |\n       |                                                               |\n       |                                                               |\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n       |                                                               |\n       |                  link-address (IPv6 address)                  |\n       |                                                               |\n       |                                                               |\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n       |                              ...                              |\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    option-code\n        OPTION_LQ_CLIENT_LINK (48)\n\n    option-len\n        Length of the list of links in octets;\n        must be a multiple of 16.\n\n    link-address\n        A global address used by the server to\n        identify the link on which the client is\n        located.\n\n    A server may respond to a query by client-id, where the 0::0 link-\n    address was specified, with this option if the client is found to be\n    on multiple links.  The requestor may then repeat the query once for\n    each link-address returned in the list, specifying the returned link-\n    address.  If the client is on a single link, the server SHOULD return\n    the client's data in an OPTION_CLIENT_DATA option.\n\n    :type link_addresses: List[IPv6Address]\n    "
    option_type = OPTION_LQ_CLIENT_LINK

    def __init__(self, link_addresses: Iterable[IPv6Address]=None):
        self.link_addresses = list(link_addresses or [])

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.link_addresses, list) or any([not isinstance(link_address, IPv6Address) or link_address.is_loopback or link_address.is_multicast or link_address.is_unspecified for link_address in self.link_addresses]):
            raise ValueError('Link addresses must be a list of valid IPv6 addresses')

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset, option_len = self.parse_option_header(buffer, offset, length, min_length=0)
        header_offset = my_offset
        self.link_addresses = []
        max_offset = option_len + header_offset
        while max_offset >= my_offset + 16:
            link_address = IPv6Address(buffer[offset + my_offset:offset + my_offset + 16])
            self.link_addresses.append(link_address)
            my_offset += 16

        if my_offset != max_offset:
            raise ValueError('Option length does not match the combined length of the parsed options')
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        buffer = bytearray()
        buffer.extend(pack('!HH', self.option_type, len(self.link_addresses) * 16))
        for link_address in self.link_addresses:
            buffer.extend(link_address.packed)

        return buffer


LeasequeryMessage.add_may_contain(ClientIdOption, min_occurrence=1)
LeasequeryMessage.add_may_contain(ServerIdOption)
LeasequeryMessage.add_may_contain(LQQueryOption, min_occurrence=1, max_occurrence=1)
LeasequeryMessage.add_may_contain(OptionRequestOption)
LeasequeryMessage.add_may_contain(StatusCodeOption)
LeasequeryReplyMessage.add_may_contain(ClientIdOption, min_occurrence=1, max_occurrence=1)
LeasequeryReplyMessage.add_may_contain(ServerIdOption, min_occurrence=1, max_occurrence=1)
LeasequeryReplyMessage.add_may_contain(ClientDataOption, max_occurrence=1)
LeasequeryReplyMessage.add_may_contain(LQRelayDataOption)
LeasequeryReplyMessage.add_may_contain(LQClientLink)
LeasequeryReplyMessage.add_may_contain(StatusCodeOption)
LQQueryOption.add_may_contain(IAAddressOption)
LQQueryOption.add_may_contain(ClientIdOption)
LQQueryOption.add_may_contain(OptionRequestOption)
ClientDataOption.add_may_contain(Option)
LQRelayDataOption.add_may_contain(RelayForwardMessage, min_occurrence=1, max_occurrence=1)