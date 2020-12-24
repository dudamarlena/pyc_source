# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/message.py
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
from binascii import hexlify
from llbase import llsd
from template import MsgData, MsgBlockData, MsgVariableData
from msgtypes import PackFlags

class MessageBase(MsgData):
    """ 
    base representation of a message name, blocks, and variables.
    MessageBase expects a name, and args consisting of Block() instances 
    (which takes a name and kwargs)
    """
    __module__ = __name__

    def __init__(self, name, *args):
        super(Message, self).__init__(name)
        self.parse_blocks(args)

    def parse_blocks(self, block_list):
        """ parse the Block() instances in the args """
        for block in block_list:
            if type(block) == list:
                for bl in block:
                    self.add_block(bl)

            else:
                self.add_block(block)


class Block(MsgBlockData):
    """ 
    base representation of a block
    Block expects a name, and kwargs for variables (var_name = value)
    """
    __module__ = __name__

    def __init__(self, name, **kwargs):
        super(Block, self).__init__(name)
        self.__parse_vars(kwargs)

    def __parse_vars(self, var_list):
        """ parse the Variable() instances in the args"""
        for variable_name in var_list:
            variable_data = var_list[variable_name]
            variable = Variable(variable_name, variable_data)
            self.add_variable(variable)


class Variable(MsgVariableData):
    """ base representation of a Variable (purely a convenience alias of MsgVariableData)

    Variable expects a name, and data
    """
    __module__ = __name__

    def __init__(self, name, data, var_type=None):
        super(Variable, self).__init__(name, data, var_type)


class Message(MessageBase):
    """ a pyogp represention of a Second Life message """
    __module__ = __name__

    def __init__(self, name, *args):
        super(MessageBase, self).__init__(name)
        self.parse_blocks(args)
        self.original_args = args
        self.send_flags = PackFlags.LL_NONE
        self.packet_id = 0
        self.event_queue_id = 0
        self.acks = []
        self.num_acks = 0
        self.trusted = False
        self.reliable = False
        self.resent = False
        self.socket = 0
        self.retries = 1
        self.host = None
        self.expiration_time = 0
        return

    def add_ack(self, packet_id):
        self.acks.append(packet_id)
        self.num_acks += 1

    def get_var(self, block, variable):
        return self.blocks[block].vars[variable]

    def from_dict_params(self, data):
        """ build this instance from a dict """
        pass

    def to_dict(self):
        """ an dict representation of a message """
        base_repr = {'body': {}, 'message': ''}
        base_repr['message'] = self.name
        for block in self.blocks:
            for _vars in self.blocks[block]:
                new_vars = {}
                for avar in _vars.var_list:
                    this_var = _vars.get_variable(avar)
                    new_vars[this_var.name] = this_var.data

            if block in base_repr['body']:
                base_repr['body'][block].append(new_vars)
            else:
                base_repr['body'][block] = [
                 new_vars]

        return base_repr

    def from_llsd_params(self, data):
        """ build this instance from llsd """
        pass

    def to_llsd(self):
        """ an llsd representation of a message """
        return llsd.format_xml(self.as_dict())

    def data(self):
        """ a string representation of a packet """
        string = ''
        delim = '    '
        for k in self.__dict__:
            if k == 'name':
                string += '\nName: %s\n' % self.name
            if k == 'blocks':
                for ablock in self.blocks:
                    string += '%sBlock Name:%s%s\n' % (delim, delim, ablock)
                    for somevars in self.blocks[ablock]:
                        for avar in somevars.var_list:
                            zvar = somevars.get_variable(avar)
                            string += '%s%s%s:%s%s\n' % (delim, delim, zvar.name, delim, zvar)

        return string

    def __repr__(self):
        """ a string representation of a packet """
        return self.data()