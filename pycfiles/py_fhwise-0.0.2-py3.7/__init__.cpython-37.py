# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/fhwise/__init__.py
# Compiled at: 2019-10-09 11:14:37
# Size of source mod 2**32: 9963 bytes
import socket, logging, struct
from .protocol import Message
_LOGGER = logging.getLogger(__name__)

class FhwisePlayer:
    __doc__ = 'Control Fhwise player though UDP.'

    def __init__(self, addr: str, port: int=8080) -> None:
        """new a Fhwise player."""
        self.addr = addr
        self.port = port
        self._send_cmdid = 1
        self._recv_cmdid = 1

    def connect(self):
        """Connect to Fhwise device."""
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.bind(('0.0.0.0', self.port))

    def disconnect(self):
        """disconnect to Fhwise device."""
        self.udp.close()
        self._send_cmdid = 1
        self._recv_cmdid = 0

    def _send_raw_command(self, command: int, payload: bytes, ack: bool) -> bytes:
        """Send UDP data to Fhwise device."""
        send_raw = Message.build(dict(code=command, payload=payload, cmdid=(self._send_cmdid)))
        _LOGGER.debug('Send command to device: ' + bytes(send_raw).hex())
        self.udp.sendto(send_raw, (self.addr, self.port))
        if ack:
            _LOGGER.debug('start receive.')
            retval = b''
            recv_raw = self.udp.recv(1024)
            _LOGGER.debug('Received from device: ' + bytes(recv_raw).hex())
            try:
                recv = Message.parse(recv_raw)
                self._recv_cmdid = recv.cmdid
                retval = recv.payload
                self._send_cmdid += 1
                if self._send_cmdid > 255:
                    self._send_cmdid = 1
                return retval
            except:
                _LOGGER.error('Received invalid raw data(%s)' % recv_raw)

        self._send_cmdid += 1
        if self._send_cmdid > 255:
            self._send_cmdid = 1
        return b''

    def send_raw_command(self, command: int, payload: bytes=b'', ack: bool=True) -> bytes:
        self.connect()
        retval = self._send_raw_command(command, payload, ack)
        self.disconnect()
        return retval

    def send_heartbeat(self) -> str:
        """Return device model in UTF8"""
        return self.send_raw_command(192).decode('utf-8')

    def send_play_pause(self) -> bytes:
        return self.send_raw_command(193)

    def send_previous_song(self) -> bytes:
        return self.send_raw_command(194)

    def send_next_song(self) -> bytes:
        return self.send_raw_command(195)

    def get_play_mode(self) -> int:
        """
        00 00 00 00 seq play
        01 00 00 00 repeat all
        02 00 00 00 repeat single
        03 00 00 00 radom play
        """
        return int.from_bytes((self.send_raw_command(196, b'0')), byteorder='little', signed=True)

    def set_toggle_play_mode(self) -> int:
        """
        00 00 00 00 seq play
        01 00 00 00 repeat all
        02 00 00 00 repeat single
        03 00 00 00 radom play
        """
        return int.from_bytes((self.send_raw_command(196, b'1')), byteorder='little', signed=True)

    def set_volume_down(self) -> int:
        return int.from_bytes((self.send_raw_command(197, b'0')), byteorder='little', signed=True)

    def set_volume_up(self) -> int:
        return int.from_bytes((self.send_raw_command(197, b'1')), byteorder='little', signed=True)

    def get_play_status(self) -> int:
        """
        FF FF FF FF no file
        00 00 00 00 invalid
        01 00 00 00 play
        02 00 00 00 pause
        03 00 00 00 stop
        04 00 00 00 pareSync
        05 00 00 00 pareComplete
        06 00 00 00 Complete
        """
        return int.from_bytes((self.send_raw_command(198)), byteorder='little', signed=True)

    def get_current_file_length(self) -> int:
        """
        A8 27 03 00 00 00 00 00 = 3"26' = 206760ms
        """
        return int.from_bytes((self.send_raw_command(200)), byteorder='little', signed=True)

    def get_current_file_position(self) -> int:
        """
        2A 7F 00 00 00 00 00 00 = 32' = 32554ms
        """
        return int.from_bytes((self.send_raw_command(201)), byteorder='little', signed=True)

    def get_current_file_name(self) -> str:
        """
        File name in UTF-8
        30 32 20 52 45 56 45 52 01 = 02 REVER
        """
        return self.send_raw_command(202).decode('utf-8')

    def get_current_room_info(self) -> str:
        """
        File name in UTF-8
        72 6F 6F 6D 3A 3A 37 38 32 = room::782
        """
        return self.send_raw_command(203).decode('utf-8')

    def set_current_file_position(self, pos: int=0) -> int:
        """
        75 66 00 00 = 26' = 26229ms
        """
        return int.from_bytes((self.send_raw_command(204, pos.to_bytes(length=4, byteorder='little', signed=True))), byteorder='little', signed=True)

    def set_current_file_type(self, type: int=0) -> int:
        """
        1：music   2：radio   3：video   4：image
        """
        return int.from_bytes((self.send_raw_command(205, type.to_bytes(length=4, byteorder='little', signed=True))), byteorder='little', signed=True)

    def get_current_list_file_account(self) -> int:
        """
        50 00 00 00 = 80
        """
        return int.from_bytes((self.send_raw_command(206)), byteorder='little', signed=True)

    def get_current_list_file_info(self, num: int) -> str:
        """
        00 00 00 00 = first file
        30 3A 3A E5 8C 97 E4 BA AC E7 88 B1 E5 AE B6 E5 B9 BF E6 92 AD 3A 3A 30 3A 3A = Name::length::Artist
        """
        return self.send_raw_command(207, num.to_bytes(length=4, byteorder='little', signed=True)).decode('utf-8')

    def set_current_list_play_file(self, num: int) -> int:
        """
        00 00 00 00 = first file
        """
        return int.from_bytes((self.send_raw_command(208, num.to_bytes(length=4, byteorder='little', signed=True))), byteorder='little', signed=True)

    def get_current_file_artist(self) -> str:
        """
        44 65 6F 72 72 6F = Deorro
        """
        return self.send_raw_command(209).decode('utf-8')

    def set_volume_level(self, num: int) -> int:
        """
        level range 0--15
        """
        return int.from_bytes((self.send_raw_command(210, num.to_bytes(length=4, byteorder='little', signed=True))), byteorder='little', signed=True)

    def get_volume_level(self) -> int:
        """
        level range 0--15
        """
        return int.from_bytes((self.send_raw_command(211)), byteorder='little', signed=True)

    def set_room_name(self, name: str) -> str:
        """
        room name in UTF-8
        72 6F 6F 6D = room
        """
        return self.send_raw_command(212, name.encode('utf-8')).decode('utf-8')

    def set_room_number(self, number: int) -> int:
        """
        room number in UTF-8
        00 00 00 31 = '1'
        """
        return int(self.send_raw_command(213, str(number).encode('utf-8')).decode('utf-8'))

    def get_volume_source(self) -> int:
        """
        FF FF FF FF = -1
        00 00 00 00 = Local
        01 00 00 00 = ext1
        02 00 00 00 = ext2
        03 00 00 00 = BT
        04 00 00 00 = UX
        """
        return int.from_bytes((self.send_raw_command(214, ((-1)).to_bytes(length=4, byteorder='little', signed=True))), byteorder='little', signed=True)

    def set_volume_source(self, source: int) -> bytes:
        """
        FF FF FF FF = -1
        00 00 00 00 = Local
        01 00 00 00 = ext1
        02 00 00 00 = ext2
        03 00 00 00 = BT
        04 00 00 00 = UX
        """
        return int.from_bytes((self.send_raw_command(214, source.to_bytes(length=4, byteorder='little', signed=True))), byteorder='little', signed=True)

    def get_sub_area_control(self, number: int) -> str:
        """
        number range 0--3
        30 3A 3A 31 35 3A 3A 31 = '0::15::1' = area0, volume15, on
        """
        return self.send_raw_command(220, number.to_bytes(length=4, byteorder='little', signed=True)).decode('utf-8')

    def set_sub_area_control(self, number: int, volume: int, on: bool) -> str:
        """
        number range 0--3
        30 3A 3A 31 35 3A 3A 31 = area1, volume15, on
        """
        send_data = '%d::%d::%d' % (number, volume, on)
        return self.send_raw_command(221, send_data.encode('utf-8')).decode('utf-8')

    def get_eq_type(self) -> int:
        """
        00 00 00 00     nomal
        01 00 00 00     rock
        02 00 00 00     pop
        03 00 00 00     dance
        04 00 00 00     hihop
        05 00 00 00     classic
        06 00 00 00     bass
        07 00 00 00     voice
        """
        return int.from_bytes((self.send_raw_command(222)), byteorder='little', signed=True)

    def set_eq_type(self, type: int) -> bytes:
        """
        00 00 00 00     normal
        01 00 00 00     rock
        02 00 00 00     pop
        03 00 00 00     dance
        04 00 00 00     hihop
        05 00 00 00     classic
        06 00 00 00     bass
        07 00 00 00     voice
        """
        return int.from_bytes((self.send_raw_command(223, type.to_bytes(length=4, byteorder='little', signed=True))), byteorder='little', signed=True)

    def get_eq_switch(self) -> int:
        """
        00 00 00 00     off
        01 00 00 00     on
        """
        return int.from_bytes((self.send_raw_command(224)), byteorder='little', signed=True)

    def set_eq_switch(self, on: bool) -> int:
        """
        00 00 00 00     off
        01 00 00 00     on
        """
        if on:
            return int.from_bytes((self.send_raw_command(225, (1).to_bytes(length=4, byteorder='little', signed=True))), byteorder='little', signed=True)
        return int.from_bytes((self.send_raw_command(225, (0).to_bytes(length=4, byteorder='little', signed=True))), byteorder='little', signed=True)

    def set_volume_toggle_mute(self) -> bytes:
        return self.send_raw_command(227)