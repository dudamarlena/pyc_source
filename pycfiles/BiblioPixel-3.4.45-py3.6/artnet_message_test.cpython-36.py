# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/util/artnet_message_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2295 bytes
import struct, unittest
from bibliopixel.util.artnet_message import dmx_message

class DMXMessageTest(unittest.TestCase):

    def do_test(self, data, sequence=1, **kwds):
        msg = dmx_message(data=data, sequence=sequence, **kwds)
        original = Original(data, sequence, **kwds).broadcast()
        self.assertEqual(len(bytes(msg)), len(original))
        differences = []
        for i, (a, b) in enumerate(zip(bytes(msg), original)):
            if a != b:
                differences.append((i, a, b))

        self.assertEqual(bytes(msg), original)

    def test_blackout(self):
        self.do_test(bytes(512 * [0]))

    def test_trivial(self):
        self.do_test(bytes())

    def test_ramp_and_a_half(self):
        self.do_test(bytes(i % 256 for i in range(384)))


class Original:

    def __init__(self, dmxdata, packet_counter=1, net=0, subnet=0, universe=0):
        self.dmxdata = dmxdata
        self.packet_counter = packet_counter
        self.net = net
        self.subnet = subnet
        self.universe = universe

    def broadcast(self):
        data = []
        data.append('Art-Net\x00')
        data.append(struct.pack('<H', 20480))
        data.append(struct.pack('>H', 14))
        data.append(struct.pack('B', self.packet_counter))
        self.packet_counter += 1
        if self.packet_counter > 255:
            self.packet_counter = 1
        data.append(struct.pack('B', 0))
        data.append(struct.pack('<H', self.net << 8 | self.subnet << 4 | self.universe))
        data.append(struct.pack('>H', len(self.dmxdata)))
        for d in self.dmxdata:
            data.append(struct.pack('B', d))

        result = bytes()
        for token in data:
            try:
                result = result + token.encode('utf-8', 'ignore')
            except:
                result = result + token

        return result