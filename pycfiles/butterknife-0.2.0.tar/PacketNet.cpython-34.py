# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bfnet/packets/PacketNet.py
# Compiled at: 2015-11-23 15:02:13
# Size of source mod 2**32: 1224 bytes
import types
from bfnet.Net import Net

class PacketNet(Net):
    """PacketNet"""

    def __init__(self, ip, port, loop, server):
        super().__init__(ip, port, loop, server)
        self._real_handler = None

    def handle(self, butterfly):
        """
        Stub method that calls your REAL handler.

        This would normally be a coroutine, but a task will be created from
        the returned handler.
        """
        try:
            return self._real_handler(butterfly)
        except TypeError as e:
            raise TypeError('Packet handler has not been set.') from e

    def set_handler(self, func: types.GeneratorType):
        """
        Set the default Packet handler.

        This can be used as a decorator, or as a normal call.

        The handler MUST be a coroutine.

        This handler MUST be an infinite loop. Failure to do so will mean your packets will stop being
        handled after one packet arrives.
        :param func: The function to set as the handler.
        :return: Your function back.
        """
        self._real_handler = func
        return func