# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/pong.py
# Compiled at: 2018-12-17 13:18:38
# Size of source mod 2**32: 3300 bytes
"""
ping / pong payload

{timestamp: 1234567890.12345, message: 'ping'}
{timestamp: 1234567890.12345, load: (m, m5, m15}, message: 'pong'}
"""
import logging, msgpack, os, multiprocessing, time, zmq
LOG = logging.getLogger(__name__)

class PongService(object):

    def __init__(self, bind_address):
        self.bind_address = bind_address
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.REP)
        self.running = False

    def bind(self):
        LOG.info('Binding pong service: %s' % self.bind_address)
        self.socket.bind(self.bind_address)

    @staticmethod
    def validate(message):
        keys = ['timestamp', 'message']
        for k in keys:
            if k not in message:
                return False

        if message['message'] != 'ping':
            return False
        else:
            return True

    def receive(self):
        r = self.socket.recv()
        try:
            message = msgpack.unpackb(r, encoding='utf-8')
        except TypeError as type_error:
            LOG.error('Recieved unpacked, non-string type: %s : %s' % (type(r), type_error))
            return
        except msgpack.UnpackException as unpack_exception:
            LOG.error('Received invalid request: %s' % str(unpack_exception))
            return

        if not self.validate(message):
            LOG.error('Received invalid request: %s' % message)
            return
        else:
            LOG.debug('Ping received: %s' % message)
            return message

    def pong(self):
        try:
            loadavg = os.getloadavg()
        except OSError as os_error:
            LOG.error('Error getting load average: %s' % str(os_error))
            loadavg = (0.0, 0.0, 0.0)

        _packet = {'timestamp':time.time(), 
         'load':loadavg, 
         'message':'pong'}
        LOG.debug('PONG: %s' % _packet)
        self.socket.send(msgpack.packb(_packet))

    def run(self):
        while True:
            r = self.receive()
            if not r:
                pass
            else:
                self.pong()


def _spawn(bind_address):
    ping_service = PongService(bind_address)
    ping_service.bind()
    try:
        ping_service.run()
    except KeyboardInterrupt:
        pass


def spawn_pong_process(bind_address):
    p = multiprocessing.Process(target=_spawn, args=[bind_address])
    p.start()
    LOG.debug('pong service started: PID=%s' % p.pid)


if __name__ == '__main__':
    logging.basicConfig(level=(logging.DEBUG))
    ps = PongService('tcp://0.0.0.0:9004')
    ps.bind()
    ps.run()