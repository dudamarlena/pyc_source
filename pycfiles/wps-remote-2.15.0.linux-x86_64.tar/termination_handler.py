# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/termination_handler.py
# Compiled at: 2016-02-23 09:08:48
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import SocketServer, socket, threading, path, os, thread, datetime

class TerminationHandler(object):

    def __init__(self, handler):
        self._handler = handler
        HOST, PORT = ('localhost', 0)
        setattr(ThreadedTCPRequestHandler, '_handle', handler)
        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
        self.ip, self.port = server.server_address
        self._write_pid_file()
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    def _write_pid_file(self):
        pid = os.getpid()
        workdir = path.path('d:\\tmp\\wpsproc\\')
        pidfile = workdir / path.path(str(pid) + '.pid')
        if pidfile.exists():
            pidfile.remove()
        pidfile.write_lines(['cmdline=', 'pid=' + str(pid), 'start_time=' + str(datetime.datetime.now()), 'tcp_port=' + str(self.port)])


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = ('{}: {}').format(cur_thread.name, self._handle())
        self.request.sendall(response)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def clean_up1(threadedTCPRequestHandler):
    return 'clean_up1'


def clean_up2(threadedTCPRequestHandler):
    return 'clean_up2'


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print ('Received: {}').format(response)
    finally:
        sock.close()


class WatchDog(object):
    r"""
        run as service every 15 minutes

        #iterate over pids of all process bots
        for pid in path.path("d:\tmp\wpsproc\").files(): #[1.pid, 2.pid,] 
            read file:
                cmdline=...
                pid=...
                start_time=...
                tcp port=...

            if pid is running and cmdline is ok and time is expired:
                #kill
                open socket(port)
                write "kill" to socket

                
            elif pids is not running:
                del "/var/proc/wpsproc/<pid>.pid

           
    """
    pass


if __name__ == '__main__':
    th = TerminationHandler(clean_up1)
    client(th.ip, th.port, 'Hello World 1')
    client(th.ip, th.port, 'Hello World 2')
    client(th.ip, th.port, 'Hello World 3')