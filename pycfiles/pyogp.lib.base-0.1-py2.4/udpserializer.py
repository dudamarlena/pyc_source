# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/udpserializer.py
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
import struct
from logging import getLogger
from msgtypes import MsgType, MsgBlockType, EndianType
from data_packer import DataPacker
from template_dict import TemplateDictionary
from pyogp.lib.base import exc
from pyogp.lib.base.message.message_dot_xml import MessageDotXML
logger = getLogger('message.udpserializer')

class UDPMessageSerializer(object):
    """ an adpater for serializing a IUDPMessage into the UDP message format

        This class builds messages at its high level, that is, keeping
        that data in data structure form. A serializer should be used on
        the message produced by this so that it can be sent over a network. """
    __module__ = __name__

    def __init__(self, message_template=None, message_xml=None):
        """initialize the adapter"""
        self.context = None
        self.template_dict = TemplateDictionary(message_template)
        self.current_template = None
        self.packer = DataPacker()
        if not message_xml:
            self.message_xml = MessageDotXML()
        else:
            self.message_xml = message_xml
        return

    def set_current_template(self):
        """ establish the template for the current packet """
        self.current_template = self.template_dict.get_template(self.context.name)

    def serialize(self, context):
        """ Builds the message by serializing the data. Creates a packet ready
            to be sent. """
        self.context = context
        self.set_current_template()
        if not self.message_xml.validate_udp_msg(self.current_template.name):
            logger.warning("Sending '%s' over UDP, which is deprecated. Discarding." % self.current_template.name)
            return
        msg_buffer = ''
        bytes = 0
        msg_buffer += self.packer.pack_data(self.context.send_flags, MsgType.MVT_U8)
        msg_buffer += self.packer.pack_data(self.context.packet_id, MsgType.MVT_S32, endian_type=EndianType.BIG)
        msg_buffer += self.packer.pack_data(0, MsgType.MVT_U8)
        if self.current_template == None:
            return
        pack_freq_num = self.current_template.msg_num_hex
        msg_buffer += pack_freq_num
        bytes += len(pack_freq_num)
        for block in self.current_template.get_blocks():
            (packed_block, block_size) = self.build_block(block, context)
            msg_buffer += packed_block
            bytes += block_size

        if self.current_template.name == 'RegionHandshakeReply':
            msg_buffer += struct.pack('>I', 0)
        self.message_buffer = msg_buffer
        return msg_buffer

    def build_block(self, template_block, message_data):
        block_buffer = ''
        bytes = 0
        block_list = message_data.get_block(template_block.name)
        block_count = len(block_list)
        if template_block.block_type == MsgBlockType.MBT_MULTIPLE:
            if template_block.number != block_count:
                raise exc.MessageSerializationError(template_block.name, 'block data mismatch')
        if template_block.block_type == MsgBlockType.MBT_VARIABLE:
            block_buffer += struct.pack('>B', block_count)
            bytes += 1
        for block in block_list:
            for v in template_block.get_variables():
                variable = block.get_variable(v.name)
                var_size = v.size
                var_data = variable.data
                data = self.packer.pack_data(var_data, v.type)
                if variable == None:
                    raise exc.MessageSerializationError(variable.name, 'variable value is not set')
                if v.type == MsgType.MVT_VARIABLE:
                    if var_size == 1:
                        block_buffer += self.packer.pack_data(len(data), MsgType.MVT_U8)
                    elif var_size == 2:
                        block_buffer += self.packer.pack_data(len(data), MsgType.MVT_U16)
                    elif var_size == 4:
                        block_buffer += self.packer.pack_data(len(data), MsgType.MVT_U32)
                    else:
                        raise exc.MessageSerializationError('variable size', 'unrecognized variable size')
                    bytes += var_size
                block_buffer += data
                bytes += len(data)

        return (
         block_buffer, bytes)