# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\multiprocessing\examples\mp_webserver.py
# Compiled at: 2009-07-30 09:32:52
import os, sys
from multiprocessing import Process, current_process, freeze_support
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
if sys.platform == 'win32':
    import multiprocessing.reduction

def note(format, *args):
    sys.stderr.write('[%s]\t%s\n' % (current_process().name, format % args))


class RequestHandler(SimpleHTTPRequestHandler):
    __module__ = __name__

    def log_message(self, format, *args):
        note(format, *args)


def serve_forever(server):
    note('starting server')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def runpool(address, number_of_processes):
    server = HTTPServer(address, RequestHandler)
    for i in range(number_of_processes - 1):
        Process(target=serve_forever, args=(server,)).start()

    serve_forever(server)


def test():
    DIR = os.path.join(os.path.dirname(__file__), '..')
    ADDRESS = ('localhost', 8000)
    NUMBER_OF_PROCESSES = 4
    print 'Serving at http://%s:%d using %d worker processes' % (ADDRESS[0], ADDRESS[1], NUMBER_OF_PROCESSES)
    print 'To exit press Ctrl-' + ['C', 'Break'][(sys.platform == 'win32')]
    os.chdir(DIR)
    runpool(ADDRESS, NUMBER_OF_PROCESSES)


if __name__ == '__main__':
    freeze_support()
    test()