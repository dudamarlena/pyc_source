# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\superpy\scripts\CleanOldTasks.py
# Compiled at: 2010-06-04 07:07:11
"""Script to clean out old tasks from server on current machine.
"""
import logging, socket, time, Servers, PicklingXMLRPC

def Go(host=None, port=None, allowedLag=86400):
    """Run the script."""
    if host == None:
        host = socket.gethostname()
    if port == None:
        port = Servers.BasicRPCServer.defaultPort
    logging.info('Making connection to %s' % [host, port])
    connection = PicklingXMLRPC.PicklingServerProxy('http://%s:%i' % (host, port))
    result = connection.CleanOldTasks(allowedLag)
    print 'Cleaned:\n' + ('\n').join(map(str, result))
    return


if __name__ == '__main__':
    logging.getLogger('').setLevel(logging.INFO)
    Go()
    pause = 3600
    print 'Pausing for %i seconds' % pause
    time.sleep(pause)