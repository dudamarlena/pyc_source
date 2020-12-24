# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moul/Git/moul/advanced-ssh-config/venv2.6/lib/python2.6/site-packages/advanced_ssh_config/network.py
# Compiled at: 2014-11-19 04:33:06
import fcntl, os, select, sys, socket, logging

class Socket(object):

    def __init__(self, hostname, port, bufsize=4096, stdin=None, stdout=None):
        self.hostname = hostname
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bufsize = bufsize
        self.logger = logging.getLogger('assh.Socket')
        if not stdin:
            stdin = sys.stdin
        if not stdout:
            stdout = sys.stdout
        self.stdin = stdin
        self.stdout = stdout

    def run(self):
        self.socket.connect((self.hostname, self.port))
        self.communicate()

    def communicate(self):
        self.socket.setblocking(0)
        fd = sys.stdin.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        inputs = [
         self.socket, self.stdin]
        while True:
            (read_ready, write_ready, in_error) = select.select(inputs, [], [])
            for sock in read_ready:
                if sock == self.stdin:
                    buffer = self.stdin.read(self.bufsize)
                    try:
                        while buffer != '':
                            self.socket.send(buffer)
                            buffer = self.stdin.read(self.bufsize)

                    except:
                        pass

                else:
                    try:
                        buffer = self.socket.recv(self.bufsize)
                        while buffer != '':
                            self.stdout.write(buffer)
                            self.stdout.flush()
                            buffer = self.socket.recv(self.bufsize)

                        if buffer == '':
                            self.logger.warn('Server disconnected')
                            return
                    except socket.error:
                        pass