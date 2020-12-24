# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext/applications/itunes_gateway.py
# Compiled at: 2009-05-11 19:02:38
"""
This application translates pings from the itunes NowPlaying plugin and translates them into 
a format that Simplecast can understand. Additionally it ignores events that take place during
a google calendar scheduled event.
"""
import time, os, BaseHTTPServer
from nowandnext.gateway.gatewayhandler import gatewayhandler
from nowandnext.utils.cmdline import cmdline
HOST_NAME = 'localhost'
PORT_NUMBER = 8181

class itunes_gateway(cmdline):
    """
    The main implementation goes here.
    """

    @classmethod
    def main(self):
        server_class = BaseHTTPServer.HTTPServer
        httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
        print time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

        httpd.server_close()
        print time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER)


def main():
    itunes_gateway.main()


if __name__ == '__main__':
    main()