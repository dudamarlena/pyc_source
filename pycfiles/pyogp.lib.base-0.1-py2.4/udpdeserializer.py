# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/udpdeserializer.py
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
from pyogp.lib.base.settings import Settings
from pyogp.lib.base.message.message_handler import MessageHandler
from template_dict import TemplateDictionary
from template import MsgData, MsgBlockData, MsgVariableData
from msgtypes import MsgType, MsgBlockType, MsgFrequency, PacketLayout, EndianType, PackFlags, sizeof
from data_unpacker import DataUnpacker
from message import Message
from pyogp.lib.base.message.message_dot_xml import MessageDotXML
from pyogp.lib.base import exc
logger = getLogger('message.udpdeserializer')

class UDPMessageDeserializer(object):
    __module__ = __name__

    def __init__(self, message_handler=None, settings=None, message_template=None, message_xml=None):
        self.context = None
        self.unpacker = DataUnpacker()
        self.current_template = None
        self.current_block = None
        self.template_dict = TemplateDictionary(message_template=message_template)
        if settings != None:
            self.settings = settings
        else:
            self.settings = Settings()
        if not message_xml:
            self.message_xml = MessageDotXML()
        else:
            self.message_xml = message_xml
        if message_handler != None:
            self.message_handler = message_handler
        elif self.settings.HANDLE_PACKETS:
            self.message_handler = MessageHandler()
        return

    def deserialize(self, context):
        self.context = context
        temp_acks = []
        msg_buff = self.context
        msg_len = len(msg_buff)
        if ord(msg_buff[0]) & PackFlags.LL_ACK_FLAG:
            num_acks = ord(msg_buff[(msg_len - 1)])
            ack_length = 1 + sizeof(MsgType.MVT_U32) * num_acks
            temp_acks = msg_buff[-ack_length:]
            msg_buff = msg_buff[:-ack_length]
        if ord(msg_buff[0]) & PackFlags.LL_ZERO_CODE_FLAG:
            offset = ord(msg_buff[5])
            header = msg_buff[:6 + offset]
            inputbuf = msg_buff[6 + offset:]
            input_len = len(inputbuf)
            msg_buff = self.zero_code_expand(inputbuf, input_len)
            msg_buff = header + msg_buff
        if self.__validate_message(msg_buff) == True:
            msg_buff = msg_buff + ('').join(temp_acks)
            if not self.message_xml.validate_udp_msg(self.current_template.name):
                logger.warning("Received '%s' over UDP, when it should come over the event queue. Discarding." % self.current_template.name)
                return
            if self.message_handler.is_message_handled(self.current_template.name) or not self.settings.ENABLE_DEFERRED_PACKET_PARSING:
                try:
                    return self.__decode_data(msg_buff)
                except exc.DataUnpackingError, error:
                    raise exc.MessageDeserializationError(self.current_template.name, error)
                    return

            elif self.settings.LOG_VERBOSE and self.settings.ENABLE_UDP_LOGGING and self.settings.LOG_SKIPPED_PACKETS and not self.settings.PROXY_LOGGING:
                logger.debug('Received packet : %s (Skipping)' % self.current_template.name)
        return

    def __validate_message(self, message_buffer):
        """ Determines if the message follows a given template. """
        if self.__decode_template(message_buffer) == True:
            return True
        return False

    def __decode_template(self, message_buffer):
        """ Determines the template that the message in the buffer
            appears to be using. """
        if PacketLayout.PACKET_ID_LENGTH >= len(message_buffer):
            raise exc.MessageDeserializationError('packet length', 'template mismatch')
        header = message_buffer[PacketLayout.PACKET_ID_LENGTH:12]
        self.current_template = self.__decode_header(header)
        if self.current_template != None:
            return True
        logger.info("Received unknown packet: '%s', packet is not in our message_template" % header)
        return False

    def __decode_header(self, header):
        frequency = self.__decode_frequency(header)
        num = self.__decode_num(header)
        result = self.template_dict.get_template_by_pair(frequency, num)
        return result

    def __decode_frequency(self, header):
        if header[0] == b'\xff':
            if header[1] == b'\xff':
                if header[2] == b'\xff':
                    return 'Fixed'
                else:
                    return 'Low'
            else:
                return 'Medium'
        else:
            return 'High'
        return

    def __decode_num(self, header):
        frequency = self.__decode_frequency(header)
        if frequency == 'Low':
            return struct.unpack('>H', header[2:4])[0]
        elif frequency == 'Medium':
            return struct.unpack('>B', header[1:2])[0]
        elif frequency == 'High':
            return struct.unpack('>B', header[0])[0]
        elif frequency == 'Fixed':
            return struct.unpack('>B', header[3:4])[0]
        else:
            return
        return

    def __decode_data(self, data):
        if self.current_template == None:
            raise exc.MessageTemplateNotFound('deserializing data')
        msg_data = MsgData(self.current_template.name)
        packet = Message(msg_data)
        msg_size = len(data)
        packet.name = self.current_template.name
        packet.send_flags = ord(data[0])
        packet.packet_id = self.unpacker.unpack_data(data, MsgType.MVT_U32, 1, endian_type=EndianType.BIG)
        if packet.send_flags & PackFlags.LL_ACK_FLAG:
            msg_size -= 1
            acks = self.unpacker.unpack_data(data, MsgType.MVT_U8, msg_size)
            ack_start = acks * sizeof(MsgType.MVT_U32)
            ack_data = data[msg_size - ack_start:]
            ack_pos = 0
            while acks > 0:
                ack_packet_id = self.unpacker.unpack_data(ack_data, MsgType.MVT_U32, start_index=ack_pos)
                ack_pos += sizeof(MsgType.MVT_U32)
                packet.add_ack(ack_packet_id)
                acks -= 1

        if packet.send_flags & PackFlags.LL_RELIABLE_FLAG:
            packet.reliable = True
        if packet.send_flags & PackFlags.LL_RESENT_FLAG:
            pass
        offset = self.unpacker.unpack_data(data, MsgType.MVT_U8, PacketLayout.PHL_OFFSET)
        freq_bytes = self.current_template.frequency
        if freq_bytes == -1:
            freq_bytes = 4
        decode_pos = PacketLayout.PACKET_ID_LENGTH + freq_bytes + offset
        for block in self.current_template.blocks:
            repeat_count = 0
            if block.block_type == MsgBlockType.MBT_SINGLE:
                repeat_count = 1
            elif block.block_type == MsgBlockType.MBT_MULTIPLE:
                repeat_count = block.number
            elif block.block_type == MsgBlockType.MBT_VARIABLE:
                repeat_count = self.unpacker.unpack_data(data, MsgType.MVT_U8, decode_pos)
                decode_pos += 1
            else:
                logger.warning('ERROR: Unknown block type: %s in %s packet.' % (str(block.block_type), packet.name))
                return
            for i in range(repeat_count):
                block_data = MsgBlockData(block.name)
                block_data.block_number = i
                self.current_block = block_data
                msg_data.add_block(self.current_block)
                for variable in block.variables:
                    var_size = variable.size
                    if variable.type == MsgType.MVT_VARIABLE:
                        data_size = var_size
                        templen = len(data)
                        if decode_pos + data_size > templen:
                            logger.warning('ERROR: trying to read %s from a buffer of len %s in %s' % (str(decode_pos + var_size), str(len(data)), packet.name))
                            return
                        if data_size == 1:
                            var_size = self.unpacker.unpack_data(data, MsgType.MVT_U8, decode_pos)
                        elif data_size == 2:
                            var_size = self.unpacker.unpack_data(data, MsgType.MVT_U16, decode_pos)
                        elif data_size == 4:
                            var_size = self.unpacker.unpack_data(data, MsgType.MVT_U32, decode_pos)
                        else:
                            raise exc.MessageDeserializationError('variable', 'unknown data size')
                        decode_pos += data_size
                    if decode_pos + var_size > len(data):
                        print var_size
                        logger.warning('ERROR: trying to read %s from a buffer of len %s in %s' % (str(decode_pos + var_size), str(len(data)), packet.name))
                        return
                    try:
                        unpacked_data = self.unpacker.unpack_data(data, variable.type, decode_pos, var_size=var_size)
                    except Exception, e:
                        logger.error('Problem parsing data in %s for %s:%s. Parameters were: Len(data):%s Type:%s decode_pos:%s var_size:%s' % (packet.name, block.name, variable.name, len(data), variable.type, decode_pos, var_size))
                        raise

                    if variable.type == MsgType.MVT_VARIABLE and variable.name != 'Data':
                        unpacked_data = unpacked_data.rstrip('\x00')
                    var_data = MsgVariableData(variable.name, unpacked_data, variable.type)
                    self.current_block.add_variable(var_data)
                    decode_pos += var_size

        if len(msg_data.blocks) <= 0 and len(self.current_template.blocks) > 0:
            raise exc.MessageDeserializationError('message', 'message is empty')
        packet.blocks = msg_data.blocks
        return packet

    def zero_code_expand(self, msg_buf, msg_size):
        """made this call more generic due to changes in how zero_code_expand is called. 
        no more header issues in actual call. Its taken care of earlier in process"""
        inputbuf = msg_buf[:]
        newstring = ''
        in_zero = False
        for c in inputbuf:
            if c != '\x00':
                if in_zero == True:
                    zero_count = ord(c)
                    zero_count = zero_count - 1
                    while zero_count > 0:
                        newstring = newstring + '\x00'
                        zero_count = zero_count - 1

                    in_zero = False
                else:
                    newstring = newstring + c
            else:
                newstring = newstring + c
                in_zero = True

        return newstring