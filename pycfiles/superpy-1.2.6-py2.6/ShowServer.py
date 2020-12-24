# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\superpy\scripts\ShowServer.py
# Compiled at: 2010-06-04 07:07:11
"""Script to show what is happening with server on current machine.
"""
import logging, socket, time
from superpy.core import Servers, PicklingXMLRPC

def Show(host=None, port=None):
    """Show all tasks running on given host and port.

    If host and port are None, we use localhost and default superpy server port.
    """
    if host == None:
        host = socket.gethostname()
    if port == None:
        port = Servers.BasicRPCServer.defaultPort
    logging.debug('Making connection to %s' % [host, port])
    connection = PicklingXMLRPC.PicklingServerProxy('http://%s:%i' % (host, port))
    result = connection.ShowQueue()
    print 'Result = ' + ('\n').join(map(str, result))
    return


if __name__ == '__main__':
    logging.getLogger('').setLevel(0)
    Show()
    pause = 3600
    print 'Pausing for %i seconds' % pause
    time.sleep(pause)