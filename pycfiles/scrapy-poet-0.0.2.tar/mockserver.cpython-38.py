# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kmike/svn/scrapy-poet/tests/mockserver.py
# Compiled at: 2020-04-27 13:38:41
# Size of source mod 2**32: 1657 bytes
import argparse, socket, sys, time
from subprocess import Popen, PIPE
from importlib import import_module
from twisted.internet import reactor
from twisted.web.server import Site

def get_ephemeral_port():
    s = socket.socket()
    s.bind(('', 0))
    return s.getsockname()[1]


class MockServer:

    def __init__(self, resource, port=None):
        self.resource = '{}.{}'.format(resource.__module__, resource.__name__)
        self.proc = None
        host = socket.gethostbyname(socket.gethostname())
        self.port = port or get_ephemeral_port()
        self.root_url = 'http://%s:%d' % (host, self.port)

    def __enter__(self):
        self.proc = Popen([
         sys.executable, '-u', '-m', 'tests.mockserver',
         self.resource, '--port', str(self.port)],
          stdout=PIPE)
        self.proc.stdout.readline()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.proc.kill()
        self.proc.wait()
        time.sleep(0.2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('resource')
    parser.add_argument('--port', type=int)
    args = parser.parse_args()
    module_name, name = args.resource.rsplit('.', 1)
    sys.path.append('.')
    resource = getattr(import_module(module_name), name)()
    http_port = reactor.listenTCP(args.port, Site(resource))

    def print_listening():
        host = http_port.getHost()
        print('Mock server {} running at http://{}:{}'.format(resource, host.host, host.port))

    reactor.callWhenRunning(print_listening)
    reactor.run()


if __name__ == '__main__':
    main()