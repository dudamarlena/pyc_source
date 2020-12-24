# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/redpitaya_client.py
# Compiled at: 2017-08-29 09:44:06
import numpy as np, socket, logging
try:
    from pysine import sine
except:

    def sine(frequency, duration):
        print 'Called sine(frequency=%f, duration=%f)' % (frequency, duration)


from .hardware_modules.dsp import dsp_addr_base, DSP_INPUTS
from .pyrpl_utils import time
CLIENT_NUMBER = 0

class MonitorClient(object):

    def __init__(self, hostname='192.168.1.0', port=2222, restartserver=None):
        """initiates a client connected to monitor_server

        hostname: server address, e.g. "localhost" or "192.168.1.0"
        port:    the port that the server is running on. 2222 by default
        restartserver: a function to call that restarts the server in case of problems
        """
        global CLIENT_NUMBER
        self.logger = logging.getLogger(name=__name__)
        CLIENT_NUMBER += 1
        self.client_number = CLIENT_NUMBER
        self.logger.debug('Client number %s started', self.client_number)
        self._restartserver = restartserver
        self._hostname = hostname
        self._port = port
        self._read_counter = 0
        self._write_counter = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for i in range(5):
            if not self._port > 0:
                if self._port is None:
                    raise ValueError('Connection to hostname %s failed. Please check your connection parameters!' % self._hostname)
                else:
                    raise ValueError('Trying to open MonitorClient for hostname %s on invalid port %s. Please check your connection parameters!' % (
                     self._hostname, self._port))
            try:
                self.socket.connect((self._hostname, self._port))
            except socket.error:
                self.logger.warning('Socket error during connection attempt %s.', i)
                self._port = self._restartserver()
            else:
                break

        self.socket.settimeout(1.0)
        return

    def close(self):
        try:
            self.socket.send('c' + bytes(bytearray([0, 0, 0, 0, 0, 0, 0])))
            self.socket.close()
        except socket.error:
            return

    def __del__(self):
        self.close()

    def reads(self, addr, length):
        self._read_counter += 1
        if hasattr(self, '_sound_debug') and self._sound_debug:
            sine(440, 0.05)
        return self.try_n_times(self._reads, addr, length)

    def writes(self, addr, values):
        self._write_counter += 1
        if hasattr(self, '_sound_debug') and self._sound_debug:
            sine(880, 0.05)
        return self.try_n_times(self._writes, addr, values)

    def _reads(self, addr, length):
        if length > 65535:
            length = 65535
            self.logger.warning('Maximum read-length is %d', length)
        header = 'r' + bytes(bytearray([0,
         length & 255, length >> 8 & 255,
         addr & 255, addr >> 8 & 255, addr >> 16 & 255, addr >> 24 & 255]))
        self.socket.send(header)
        data = self.socket.recv(length * 4 + 8)
        while len(data) < length * 4 + 8:
            data += self.socket.recv(length * 4 - len(data) + 8)

        if data[:8] == header:
            return np.frombuffer(data[8:], dtype=np.uint32)
        else:
            self.logger.error('Wrong control sequence from server: %s', data[:8])
            self.emptybuffer()
            return
            return

    def _writes(self, addr, values):
        values = values[:65533]
        length = len(values)
        header = 'w' + bytes(bytearray([0,
         length & 255,
         length >> 8 & 255,
         addr & 255,
         addr >> 8 & 255,
         addr >> 16 & 255,
         addr >> 24 & 255]))
        self.socket.send(header + np.array(values, dtype=np.uint32).tobytes())
        if self.socket.recv(8) == header:
            return True
        else:
            self.logger.error('Error: wrong control sequence from server')
            self.emptybuffer()
            return
            return

    def emptybuffer(self):
        for i in range(100):
            n = len(self.socket.recv(16384))
            if n <= 0:
                return
            self.logger.debug('Read %d bytes from socket...', n)

    def try_n_times(self, function, addr, value, n=5):
        for i in range(n):
            try:
                value = function(addr, value)
            except (socket.timeout, socket.error):
                self.logger.error('Error occured in reading attempt %s. Reconnecting at addr %s to %s value %s by client %s' % (
                 i,
                 hex(addr),
                 function.__name__,
                 value,
                 self.client_number))
                if self._restartserver is not None:
                    self.restart()
            else:
                if value is not None:
                    return value

        return

    def restart(self):
        self.close()
        port = self._restartserver()
        self.__init__(hostname=self._hostname, port=port, restartserver=self._restartserver)


class DummyClient(object):
    """Class for unitary tests without RedPitaya hardware available"""

    class fpgadict(dict):

        def __missing__(self, key):
            return 1

    fpgamemory = fpgadict({str(1074790420): 1})

    def read_fpgamemory(self, addr):
        offset = addr - 1074790400
        if offset >= 65536 and offset < 196608:
            v = int(np.random.normal(scale=8191)) // 4
            if v > 8191:
                v = 25
            elif v < -8191:
                v = -8191
            if v < 0:
                v += 16384
            return v
        if offset == 0:
            return 0
        if offset == 348:
            t = int(time() * 125000000.0)
            return t % 4294967296
        if offset == 352:
            return 0
            t = int(time() * 125000000.0)
            return t - t % 4294967296
        if offset == 356:
            return 0
        if offset == 360:
            return 0
        all = DSP_INPUTS
        for module in DSP_INPUTS:
            offset = addr - dsp_addr_base(module)
            if module.startswith('pid'):
                if offset == 544:
                    return 4
                if offset == 552:
                    return 1
            else:
                if module.startswith('iir'):
                    if offset == 512:
                        return 64
                    if offset == 516:
                        return 32
                    if offset == 520:
                        return 16
                    if offset == 544:
                        return 1
                    if offset == 264:
                        return 0
                elif module.startswith('iq'):
                    if offset == 544:
                        return 1
                    if offset == 560:
                        return 2
                    if offset == 564:
                        return 2
                    if offset == 568:
                        return 1
                for filter_module in ['iq', 'pid', 'iir']:
                    if module.startswith(filter_module):
                        if offset == 544:
                            return 1
                        if offset == 548:
                            return 2
                        if offset == 552:
                            return 1

        return self.fpgamemory[str(addr)]

    def reads(self, addr, length):
        val = []
        for i in range(length):
            val.append(self.read_fpgamemory(addr + 4 * i))

        return np.array(val, dtype=np.uint32)

    def writes(self, addr, values):
        for i, v in enumerate(values):
            self.fpgamemory[str(addr + 4 * i)] = v

    def restart(self):
        pass

    def close(self):
        pass