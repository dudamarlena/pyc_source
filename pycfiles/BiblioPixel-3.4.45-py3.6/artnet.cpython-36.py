# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/artnet.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1137 bytes
import copy, ctypes, enum
from .server_driver import ServerDriver
from ..util import artnet_message, log, offset_range, server_cache, udp

class ArtNet(ServerDriver):
    SERVER_CLASS = udp.Sender

    def __init__(self, *args, ip_address='', port=artnet_message.UDP_PORT, filter_dupes=True, offset=0, **kwds):
        """
        :param dict channel_map: maps DMX channels to positions in
            the color_list
        :param int offset: a DMX channel offset, positive, negative or zero
        """
        (super().__init__)(args, address=(ip_address, port), **kwds)
        self.filter_dupes = filter_dupes
        self.offset = offset_range.DMXChannel(offset)
        self.msg = artnet_message.dmx_message()
        self.last_message = None

    def _send_packet(self):
        self._copy_buffer_into_data()
        msg = bytes(self.msg)
        if not (self.filter_dupes and msg == self.last_message):
            self.server.send(msg)
            self.last_message = msg

    def _copy_buffer_into_data(self):
        self.offset.copy_to(self._buf, self.msg.data)

    def _on_positions(self):
        pass