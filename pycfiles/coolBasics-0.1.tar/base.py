# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/coolamqp/framing/base.py
# Compiled at: 2020-05-06 12:56:42
from __future__ import absolute_import, division, print_function
import typing as tp
AMQP_HELLO_HEADER = 'AMQP\x00\x00\t\x01'
BASIC_TYPES = {'bit': (None, None, '0', None), 'octet': (1, 'B', "b'\\x00'", 1), 
   'short': (2, 'H', "b'\\x00\\x00'", 2), 
   'long': (4, 'I', "b'\\x00\\x00\\x00\\x00'", 4), 
   'longlong': (8, 'Q', "b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'", 8), 
   'timestamp': (8, 'Q', "b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'", 8), 
   'table': (None, None, "b'\\x00\\x00\\x00\\x00'", 4), 
   'longstr': (None, None, "b'\\x00\\x00\\x00\\x00'", 4), 
   'shortstr': (None, None, "b'\\x00'", 1)}
DYNAMIC_BASIC_TYPES = ('table', 'longstr', 'shortstr')

class AMQPFrame(object):
    FRAME_TYPE = None

    def __init__(self, channel):
        self.channel = channel

    def write_to(self, buf):
        """
        Write a complete frame to buffer

        This writes type and channel ID.
        """
        raise NotImplementedError('Please write the frame type and channel in child classes, its faster that way ')

    @staticmethod
    def unserialize(channel, payload_as_buffer):
        """
        Unserialize from a buffer.
        Buffer starts at frame's own payload - type, channel and size was already obtained.
        Payload does not contain FRAME_EMD.
        AMQPHeartbeatFrame does not have to implement this.
        """
        raise NotImplementedError('Override me')

    def get_size(self):
        """
        Return size of this frame, in bytes, from frame type to frame_end
        :return: int
        """
        raise NotImplementedError('Override me')

    def __str__(self):
        return 'AMQPFrame(%s)' % (self.channel,)


class AMQPPayload(object):
    """Payload is something that can write itself to bytes,
    or at least provide a buffer to do it."""
    __slots__ = ()

    def write_to(self, buf):
        """
        Emit itself into a buffer, from length to FRAME_END

        :param buf: buffer to write to (will be written using .write)
        """
        pass

    def get_size(self):
        """
        Return size of this payload
        :return: int
        """
        raise NotImplementedError()


class AMQPClass(object):
    """An AMQP class"""
    __slots__ = ()


class AMQPContentPropertyList(object):
    """
    A class is intmately bound with content and content properties.

    WARNING: BE PREPARED that if you receive a content from the network,
    string values will be memoryviews. Use .tobytes() to correct that.
    If YOU create a property list, they will be bytes all right.
    """
    PROPERTIES = []

    def __str__(self):
        return '<AMQPContentPropertyList>'

    def get(self, property_name, default=None):
        """
        Return a particular property, or default if not defined

        :param property_name: property name, unicode
        :param default: default value
        :return: memoryview or bytes
        """
        return getattr(self, property_name, default)

    @staticmethod
    def zero_property_flags(property_flags):
        """
        Given a binary property_flags, set all bit properties to 0.

        This leaves us with a canonical representation, that can be used
        in obtaining a particular property list

        :param property_flags: binary
        :return: binary
        """
        return property_flags

    def write_to(self, buf):
        """Serialize itself (flags + values) to a buffer"""
        raise Exception('This is an abstract method')

    @staticmethod
    def from_buffer(self, buf, start_offset):
        """
        Return an instance of self, loaded from a buffer.

        This does not have to return length, because it is always passed exactly enough of a buffer.

        Buffer HAS TO start at property_flags
        """
        raise Exception('This is an abstract method')

    def get_size(self):
        """
        How long is property_flags + property_values

        :return: int
        """
        raise Exception('This is an abstract method')


class AMQPMethodPayload(AMQPPayload):
    __slots__ = ()
    RESPONSE_TO = None
    REPLY_WITH = []
    FIELDS = []

    def get_size(self):
        """
        Calculate the size of this frame.

        Needs to be overloaded, unless you're a class with IS_CONTENT_STATIC

        :return: int, size of argument section
        :raises RuntimeError: this class isn't IS_CONTENT_STATIC and this method was called directly.
            In this case, you should have rather subclassed it.
        """
        if self.IS_CONTENT_STATIC:
            return len(self.STATIC_CONTENT) - 4 - 4 - 1
        raise RuntimeError('Should never be executed!')

    def write_arguments(self, buf):
        """
        Write the argument portion of this frame into target buffer.

        :param buf: buffer to write to
        :type buf: tp.BinaryIO
        :raise ValueError: some field here is invalid!
        """
        raise NotImplementedError()

    @classmethod
    def from_buffer(cls, buf, offset):
        """
        Construct this frame from a buffer

        :param buf: a buffer to construct the frame from
        :type buf: buffer or memoryview
        :param offset: offset the argument portion begins at
        :type offset: int
        :return: an instance of this class
        :raise ValueError: invalid data
        """
        raise NotImplementedError('')