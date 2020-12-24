# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/printflow2/main_webserver.py
# Compiled at: 2014-04-03 03:33:52
# Size of source mod 2**32: 1009 bytes
__doc__ = '\nCreated on Jan 24, 2014\n\n@author: "Colin Manning"\n'
import signal, sys, traceback
from http.server import HTTPServer
from printflow2.WebServer import WebServer
__printflow2_version__ = '0.5.1'
serverName = 'localhost'
serverPort = 8087
server = None

def main():
    try:
        server = HTTPServer((serverName, serverPort), WebServer)
        print(('running printflow2 web server version: ', __printflow2_version__, ' on server: ', serverName, 'port: ', serverPort))
        server.serve_forever()
    except:
        print('Exception raised for PritnFlow 2 Web Server on server: ', serverName, ' port: ', serverPort)
        print(traceback.format_exc())
        server.socket.close()


def close_down(signal, frame):
    print('printflow2 web server is shutting down')
    server.socket.close()
    sys.exit(0)


signal.signal(signal.SIGINT, close_down)
signal.signal(signal.SIGTERM, close_down)
if __name__ == '__main__':
    main()