# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/duids.py
# Compiled at: 2017-06-24 07:05:23
# Size of source mod 2**32: 19403 bytes
"""
Classes and constants for the DUIDs defined in :rfc:`3315`
"""
from struct import pack, unpack_from
from dhcpkit.display_strings import hardware_types
from dhcpkit.protocol_element import ElementDataRepresentation, ProtocolElement
from dhcpkit.utils import normalise_hex
from typing import Union
DUID_LLT = 1
DUID_EN = 2
DUID_LL = 3

class DUID(ProtocolElement):
    __doc__ = '\n    :rfc:`3315#section-9.1`\n\n    A DUID consists of a two-octet type code represented in network byte\n    order, followed by a variable number of octets that make up the\n    actual identifier.  A DUID can be no more than 128 octets long (not\n    including the type code).\n    '
    duid_type = 0

    def __hash__(self) -> int:
        """
        Make DUIDs hashable.

        :return: The hash value
        """
        return hash(self.save())

    @classmethod
    def determine_class(cls, buffer: bytes, offset: int=0) -> type:
        """
        Return the appropriate subclass from the registry, or UnknownDUID if no subclass is registered.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :return: The best known class for this duid data
        """
        from dhcpkit.ipv6.duid_registry import duid_registry
        duid_type = unpack_from('!H', buffer, offset=offset)[0]
        return duid_registry.get(duid_type, UnknownDUID)

    def parse_duid_header(self, buffer: bytes, offset: int=0,
                          length: int=None) -> int:
        """
        Parse the DUID type and perform some basic validation.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        if not length:
            raise ValueError('DUIDs length must be explicitly provided when parsing')
        duid_type = unpack_from('!H', buffer, offset=offset)[0]
        my_offset = 2
        if duid_type != self.duid_type:
            raise ValueError('The provided buffer does not contain {} data'.format(self.__class__.__name__))
        return my_offset


class UnknownDUID(DUID):
    __doc__ = "\n    Container for raw DUID content for cases where we don't know how to decode the DUID.\n    "

    def __init__(self, duid_type: int=0,
                 duid_data: bytes=b''):
        self.duid_type = duid_type
        self.duid_data = duid_data

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
        self.duid_type = unpack_from('!H', buffer, offset=offset)[0]
        my_offset = self.parse_duid_header(buffer, offset, length)
        duid_len = length - my_offset
        self.duid_data = buffer[offset + my_offset:offset + my_offset + duid_len]
        my_offset += duid_len
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        return pack('!H', self.duid_type) + self.duid_data


class LinkLayerTimeDUID(DUID):
    __doc__ = "\n    :rfc:`3315#section-9.2`\n\n    This type of DUID consists of a two octet type field containing the\n    value 1, a two octet hardware type code, four octets containing a\n    time value, followed by link-layer address of any one network\n    interface that is connected to the DHCP device at the time that the\n    DUID is generated.  The time value is the time that the DUID is\n    generated represented in seconds since midnight (UTC), January 1,\n    2000, modulo 2^32.  The hardware type MUST be a valid hardware type\n    assigned by the IANA as described in :rfc:`826` [14].  Both the time and\n    the hardware type are stored in network byte order.  The link-layer\n    address is stored in canonical form, as described in :rfc:`2464` [2].\n\n    The following diagram illustrates the format of a DUID-LLT:\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |               1               |    hardware type (16 bits)    |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                        time (32 bits)                         |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      .                                                               .\n      .             link-layer address (variable length)              .\n      .                                                               .\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    The choice of network interface can be completely arbitrary, as long\n    as that interface provides a globally unique link-layer address for\n    the link type, and the same DUID-LLT SHOULD be used in configuring\n    all network interfaces connected to the device, regardless of which\n    interface's link-layer address was used to generate the DUID-LLT.\n\n    Clients and servers using this type of DUID MUST store the DUID-LLT\n    in stable storage, and MUST continue to use this DUID-LLT even if the\n    network interface used to generate the DUID-LLT is removed.  Clients\n    and servers that do not have any stable storage MUST NOT use this\n    type of DUID.\n\n    Clients and servers that use this DUID SHOULD attempt to configure\n    the time prior to generating the DUID, if that is possible, and MUST\n    use some sort of time source (for example, a real-time clock) in\n    generating the DUID, even if that time source could not be configured\n    prior to generating the DUID.  The use of a time source makes it\n    unlikely that two identical DUID-LLTs will be generated if the\n    network interface is removed from the client and another client then\n    uses the same network interface to generate a DUID-LLT.  A collision\n    between two DUID-LLTs is very unlikely even if the clocks have not\n    been configured prior to generating the DUID.\n\n    This method of DUID generation is recommended for all general purpose\n    computing devices such as desktop computers and laptop computers, and\n    also for devices such as printers, routers, and so on, that contain\n    some form of writable non-volatile storage.\n\n    Despite our best efforts, it is possible that this algorithm for\n    generating a DUID could result in a client identifier collision.  A\n    DHCP client that generates a DUID-LLT using this mechanism MUST\n    provide an administrative interface that replaces the existing DUID\n    with a newly-generated DUID-LLT.\n    "
    duid_type = DUID_LLT

    def __init__(self, hardware_type: int=0,
                 time: int=0, link_layer_address: bytes=b''):
        self.hardware_type = hardware_type
        self.time = time
        self.link_layer_address = link_layer_address

    def display_hardware_type(self) -> ElementDataRepresentation:
        """
        Nicer representation of hardware types
        :return: Representation of hardware type
        """
        display = hardware_types.get(self.hardware_type, 'Unknown')
        return ElementDataRepresentation('{} ({})'.format(display, self.hardware_type))

    def display_link_layer_address(self) -> Union[(ElementDataRepresentation, bytes)]:
        """
        Nicer representation of link-layer address if we know the hardware type
        :return: Representation of link-layer address
        """
        if self.hardware_type == 1:
            return ElementDataRepresentation(normalise_hex(self.link_layer_address, include_colons=True))
        else:
            return self.link_layer_address

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.hardware_type, int) or not 0 <= self.hardware_type < 65536:
            raise ValueError('Hardware type must be an unsigned 16 bit integer')
        if not isinstance(self.time, int) or not 0 <= self.time < 4294967296:
            raise ValueError('Time must be an unsigned 32 bit integer')
        if not isinstance(self.link_layer_address, bytes):
            raise ValueError('Link-layer address must be a sequence of bytes')
        if len(self.link_layer_address) > 120:
            raise ValueError('DUID-LLT link-layer address cannot be longer than 120 bytes')

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset = self.parse_duid_header(buffer, offset, length)
        self.hardware_type, self.time = unpack_from('!HI', buffer, offset=offset + my_offset)
        my_offset += 6
        ll_len = length - my_offset
        self.link_layer_address = buffer[offset + my_offset:offset + my_offset + ll_len]
        my_offset += ll_len
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        return pack('!HHI', self.duid_type, self.hardware_type, self.time) + self.link_layer_address


class EnterpriseDUID(DUID):
    __doc__ = "\n    :rfc:`3315#section-9.3`\n\n    This form of DUID is assigned by the vendor to the device.  It\n    consists of the vendor's registered Private Enterprise Number as\n    maintained by IANA [6] followed by a unique identifier assigned by\n    the vendor.  The following diagram summarizes the structure of a\n    DUID-EN:\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |               2               |       enterprise-number       |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |   enterprise-number (contd)   |                               |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                               |\n      .                           identifier                          .\n      .                       (variable length)                       .\n      .                                                               .\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    The source of the identifier is left up to the vendor defining it,\n    but each identifier part of each DUID-EN MUST be unique to the device\n    that is using it, and MUST be assigned to the device at the time it\n    is manufactured and stored in some form of non-volatile storage.  The\n    generated DUID SHOULD be recorded in non-erasable storage.  The\n    enterprise-number is the vendor's registered Private Enterprise\n    Number as maintained by IANA [6].  The enterprise-number is stored as\n    an unsigned 32 bit number.\n\n    An example DUID of this type might look like this:\n\n    .. code-block:: none\n\n      +---+---+---+---+---+---+---+---+\n      | 0 | 2 | 0 | 0 | 0 |  9| 12|192|\n      +---+---+---+---+---+---+---+---+\n      |132|221| 3 | 0 | 9 | 18|\n      +---+---+---+---+---+---+\n\n    This example includes the two-octet type of 2, the Enterprise Number\n    (9), followed by eight octets of identifier data\n    (0x0CC084D303000912).\n    "
    duid_type = DUID_EN

    def __init__(self, enterprise_number: int=0,
                 identifier: bytes=b''):
        self.enterprise_number = enterprise_number
        self.identifier = identifier

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.enterprise_number, int) or not 0 <= self.enterprise_number < 4294967296:
            raise ValueError('Enterprise number must be an unsigned 32 bit integer')
        if not isinstance(self.identifier, bytes):
            raise ValueError('Identifier must be a sequence of bytes')
        if len(self.identifier) > 122:
            raise ValueError('DUID-EN identifier cannot be longer than 122 bytes')

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset = self.parse_duid_header(buffer, offset, length)
        self.enterprise_number = unpack_from('!I', buffer, offset=offset + my_offset)[0]
        my_offset += 4
        identifier_len = length - my_offset
        self.identifier = buffer[offset + my_offset:offset + my_offset + identifier_len]
        my_offset += identifier_len
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        return pack('!HI', self.duid_type, self.enterprise_number) + self.identifier


class LinkLayerDUID(DUID):
    __doc__ = "\n    :rfc:`3315#section-9.4`\n\n    This type of DUID consists of two octets containing the DUID type 3,\n    a two octet network hardware type code, followed by the link-layer\n    address of any one network interface that is permanently connected to\n    the client or server device.  For example, a host that has a network\n    interface implemented in a chip that is unlikely to be removed and\n    used elsewhere could use a DUID-LL.  The hardware type MUST be a\n    valid hardware type assigned by the IANA, as described in :rfc:`826`\n    [14].  The hardware type is stored in network byte order.  The\n    link-layer address is stored in canonical form, as described in\n    :rfc:`2464` [2].  The following diagram illustrates the format of a\n    DUID-LL:\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |               3               |    hardware type (16 bits)    |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      .                                                               .\n      .             link-layer address (variable length)              .\n      .                                                               .\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    The choice of network interface can be completely arbitrary, as long\n    as that interface provides a unique link-layer address and is\n    permanently attached to the device on which the DUID-LL is being\n    generated.  The same DUID-LL SHOULD be used in configuring all\n    network interfaces connected to the device, regardless of which\n    interface's link-layer address was used to generate the DUID.\n\n    DUID-LL is recommended for devices that have a permanently-connected\n    network interface with a link-layer address, and do not have\n    nonvolatile, writable stable storage.  DUID-LL MUST NOT be used by\n    DHCP clients or servers that cannot tell whether or not a network\n    interface is permanently attached to the device on which the DHCP\n    client is running.\n    "
    duid_type = DUID_LL

    def __init__(self, hardware_type: int=0,
                 link_layer_address: bytes=b''):
        self.hardware_type = hardware_type
        self.link_layer_address = link_layer_address

    def display_hardware_type(self) -> ElementDataRepresentation:
        """
        Nicer representation of hardware types
        :return: Representation of hardware type
        """
        display = hardware_types.get(self.hardware_type, 'Unknown')
        return ElementDataRepresentation('{} ({})'.format(display, self.hardware_type))

    def display_link_layer_address(self) -> Union[(ElementDataRepresentation, bytes)]:
        """
        Nicer representation of link-layer address if we know the hardware type
        :return: Representation of link-layer address
        """
        if self.hardware_type == 1:
            return ElementDataRepresentation(normalise_hex(self.link_layer_address, include_colons=True))
        else:
            return self.link_layer_address

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.hardware_type, int) or not 0 <= self.hardware_type < 65536:
            raise ValueError('Hardware type must be an unsigned 16 bit integer')
        if not isinstance(self.link_layer_address, bytes):
            raise ValueError('Link-layer address must be a sequence of bytes')
        if len(self.link_layer_address) > 124:
            raise ValueError('DUID-LL link-layer address cannot be longer than 124 bytes')

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset = self.parse_duid_header(buffer, offset, length)
        self.hardware_type = unpack_from('!H', buffer, offset=offset + my_offset)[0]
        my_offset += 2
        ll_len = length - my_offset
        self.link_layer_address = buffer[offset + my_offset:offset + my_offset + ll_len]
        my_offset += ll_len
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        return pack('!HH', self.duid_type, self.hardware_type) + self.link_layer_address