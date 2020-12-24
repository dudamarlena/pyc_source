# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bfnet/packets/Packets.py
# Compiled at: 2015-12-07 14:13:35
# Size of source mod 2**32: 3163 bytes
import struct, collections
from bfnet import util

class _MetaPacket(type):
    __doc__ = '\n    This Metaclass exists only to prepare an ordered dict.\n    '

    @classmethod
    def __prepare__(mcs, name, bases):
        return collections.OrderedDict()


class BasePacket(object, metaclass=_MetaPacket):
    __doc__ = '\n    A BasePacket is the base class for all Packet types.\n\n    This just creates a few stub methods.\n    '
    id = -1
    _endianness = '>'

    def __init__(self, pbf):
        """
        Default init method.
        """
        self.butterfly = pbf

    def on_creation(self):
        """
        Called just after your packet object is created.
        """
        pass

    def create(self, data: bytes):
        """
        Create a new Packet.
        :param data: The data to use.
        :return: If the creation succeeded or not.
        """
        self.on_creation()

    def autopack(self) -> bytes:
        """
        Attempt to autopack your data correctly.

        This does two things:
            - Scan your class dictionary for all non-function and struct-packable
            items.
            - Infer their struct format type, build a format string, then pack them.
        :return: The packed bytes data.
        """
        to_fmt = []
        v = vars(self)
        for variable, val in v.items():
            if type(val) not in [bytes, str, int, float]:
                self.butterfly.logger.debug('Found un-packable type: {}, skipping'.format(type(val)))
            elif variable.startswith('_'):
                self.butterfly.logger.debug('Found private variable {}, skipping'.format(variable))
            elif variable.lower() == 'id':
                self.butterfly.logger.debug('Skipping ID variable')
            else:
                to_fmt.append(val)

        packed = util.auto_infer_struct_pack(*to_fmt, pack=True)
        return packed


class Packet(BasePacket):
    __doc__ = "\n    A standard Packet type.\n\n    This extends from BasePacket, and adds useful details that you'll want to use.\n    "

    def __init__(self, pbf):
        """
        Create a new Packet type.
        :return:
        """
        super().__init__(pbf)
        self._original_data = {}

    def create(self, data: dict) -> bool:
        """
        Create a new Packet.
        :param data: The data to use.
            This data should have the PacketButterfly header stripped.
        :return: A boolean, True if we need no more processing, and False if we process ourself.
        """
        self._original_data = data
        self.unpack(data)
        return True

    def unpack(self, data: dict) -> bool:
        """
        Unpack the data for the packet.
        :return: A boolean, if it was unpacked.
        """
        return True

    def gen(self) -> bytes:
        """
        Generate a new set of data to write to the connection.
        :return:
        """
        pass