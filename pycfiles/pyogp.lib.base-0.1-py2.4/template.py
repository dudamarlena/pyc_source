# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/template.py
# Compiled at: 2010-02-07 17:28:31
"""
Contributors can be viewed at:
http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt 

$LicenseInfo:firstyear=2008&license=apachev2$

Copyright 2009, Linden Research, Inc.

Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0
or in 
    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt

$/LicenseInfo$
"""
import struct, re, pprint, binascii
from msgtypes import MsgType, MsgBlockType

class MsgData(object):
    """ Used as a Message that is being created that will be
        serialized and sent. """
    __module__ = __name__

    def __init__(self, name):
        self.name = name
        self.size = 0
        self.blocks = {}

    def add_block(self, block):
        if block.name not in self.blocks:
            self.blocks[block.name] = []
        self.blocks[block.name].append(block)

    def get_block(self, block_name):
        return self.blocks[block_name]

    def __getitem__(self, block_name):
        return self.get_block(block_name)

    def add_data(self, block_name, var_name, data, data_size):
        get_block(block_name).add_data(var_name, data, data_size)


class MsgBlockData(object):
    """ Used as a Message block that is being created that will be
        serialized and sent. """
    __module__ = __name__

    def __init__(self, name):
        self.name = name
        self.size = 0
        self.vars = {}
        self.var_list = []
        self.block_number = 0

    def get_variable(self, var_name):
        return self.vars[var_name]

    def __getitem__(self, name):
        return self.get_variable(name).data

    def get_variables(self):
        return self.vars.values()

    def add_variable(self, var):
        self.vars[var.name] = var
        self.var_list.append(var.name)

    def __call__(self):
        return self.vars


class MsgVariableData(object):
    """ Used as a Message Block variable that is being created that will be
        serialized and sent """
    __module__ = __name__

    def __init__(self, name, data, var_type=None):
        self.name = name
        self.size = -1
        self.data = data
        self.var_type = var_type

    def get_var_type_as_string(self):
        return MsgType.MVT_as_string(self.var_type)

    def get_data_as_string(self):
        if self.var_type == MsgType.MVT_VARIABLE:
            return self.data
        elif self.var_type == MsgType.MVT_FIXED:
            return str(struct.unpack('h' * (len(self.data) / 2), self.data))
        else:
            return str(self.data)

    def __str__(self):
        return self.get_data_as_string()

    def __repr__(self):
        return self.get_data_as_string()

    def __call__(self):
        return self.data


class MessageTemplateVariable(object):
    """TODO: Add docstring"""
    __module__ = __name__

    def __init__(self, name, tp, size):
        self.name = name
        self.type = tp
        self.size = size

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_type_as_string(self):
        return MsgType.MVT_as_string(self.type)


class MessageTemplateBlock(object):
    """TODO: Add docstring"""
    __module__ = __name__

    def __init__(self, name):
        self.variables = []
        self.variable_map = {}
        self.name = name
        self.block_type = 0
        self.number = 0

    def add_variable(self, var):
        self.variable_map[var.name] = var
        self.variables.append(var)

    def get_variables(self):
        return self.variables

    def get_variable(self, name):
        return self.variable_map[name]

    def get_name(self):
        return self.name

    def get_block_type(self):
        return self.block_type

    def get_block_type_as_string(self):
        return MsgBlockType.MBT_as_string(self.block_type)

    def get_block_number(self):
        return self.number


class MessageTemplate(object):
    __module__ = __name__
    frequency_strings = {-1: 'fixed', 1: 'high', 2: 'medium', 4: 'low'}
    depecration_strings = ['Deprecated', 'UDPDeprecated', 'UDPBlackListed', 'NotDeprecated']
    encoding_strings = ['Unencoded', 'Zerocoded']
    trusted_strings = ['Trusted', 'NotTrusted']

    def __init__(self, name):
        self.blocks = []
        self.block_map = {}
        self.received_count = 0
        self.name = name
        self.frequency = None
        self.msg_num = 0
        self.msg_num_hex = None
        self.msg_trust = None
        self.msg_deprecation = None
        self.msg_encoding = None
        return

    def add_block(self, block):
        self.block_map[block.name] = block
        self.blocks.append(block)

    def get_blocks(self):
        return self.blocks

    def get_block(self, name):
        return self.block_map[name]

    def get_name(self):
        return self.name

    def get_frequency(self):
        return self.frequency

    def get_frequency_as_string(self):
        return MessageTemplate.frequency_strings[self.frequency]

    def get_message_number(self):
        return self.msg_num

    def get_message_hex_num(self):
        return ('').join([ '%02X' % ord(x) for x in self.msg_num_hex ]).strip()

    def get_message_trust(self):
        return self.msg_trust

    def get_message_trust_as_string(self):
        return MessageTemplate.trusted_strings[self.msg_trust]

    def get_message_encoding(self):
        return self.msg_encoding

    def get_message_encoding_as_string(self):
        return MessageTemplate.encoding_strings[self.msg_encoding]

    def get_deprecation(self):
        return self.msg_deprecation

    def get_deprecation_as_string(self):
        return MessageTemplate.depecration_strings[self.msg_deprecation]