# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/reflection.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 3779 bytes
"""Contains a metaclass and helper functions used to create
protocol message classes from Descriptor objects at runtime.

Recall that a metaclass is the "type" of a class.
(A class is to a metaclass what an instance is to a class.)

In this case, we use the GeneratedProtocolMessageType metaclass
to inject all the useful functionality into the classes
output by the protocol compiler at compile-time.

The upshot of all this is that the real implementation
details for ALL pure-Python protocol buffers are *here in
this file*.
"""
__author__ = 'robinson@google.com (Will Robinson)'
from google.protobuf import message_factory
from google.protobuf import symbol_database
GeneratedProtocolMessageType = message_factory._GENERATED_PROTOCOL_MESSAGE_TYPE
MESSAGE_CLASS_CACHE = {}

def ParseMessage(descriptor, byte_str):
    """Generate a new Message instance from this Descriptor and a byte string.

  DEPRECATED: ParseMessage is deprecated because it is using MakeClass().
  Please use MessageFactory.GetPrototype() instead.

  Args:
    descriptor: Protobuf Descriptor object
    byte_str: Serialized protocol buffer byte string

  Returns:
    Newly created protobuf Message object.
  """
    result_class = MakeClass(descriptor)
    new_msg = result_class()
    new_msg.ParseFromString(byte_str)
    return new_msg


def MakeClass(descriptor):
    """Construct a class object for a protobuf described by descriptor.

  DEPRECATED: use MessageFactory.GetPrototype() instead.

  Args:
    descriptor: A descriptor.Descriptor object describing the protobuf.
  Returns:
    The Message class object described by the descriptor.
  """
    return symbol_database.Default().GetPrototype(descriptor)