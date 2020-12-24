# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/api/printing/lpr.py
# Compiled at: 2012-10-12 07:02:39
import socket, random

class LPR(object):

    def __init__(self, server, user=None):
        self.server = server
        self.socket = None
        self.hostname = socket.gethostname()
        if user is None:
            self.user = 'OpenGroupware'
        else:
            self.user = user
        return

    def connect(self):
        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server, 515))
        return

    def send_stream(self, queue, name, stream, job_name=None):
        self.command_receive(queue)
        self.subcommand_receive_controlfile(name, job_name=job_name)
        self.subcommand_receive_datafile(stream)

    def close(self):
        self.socket.close()

    def wait(self):
        d = self.socket.recv(1024)
        if d != '\x00':
            raise Exception(('LPD Protocol Exception {0}').format(ord(d)))

    def command_restart(self, queue_name):
        self.queue_name = queue_name
        payload = ('\x02{0}\n').format(queue_name)
        self.socket.send(payload)
        self.wait()

    def command_close(self):
        self.socket.send('\x00')
        self.wait()

    def command_receive(self, queue_name):
        payload = ('\x02{0}\n').format(queue_name)
        self.df = ('df{0}{1}').format(str(random.randint(1000, 9999)), self.hostname)
        self.socket.send(payload)
        self.wait()

    def subcommand_abort(self):
        self.socket.send('\x01\n')
        self.wait()

    def subcommand_receive_controlfile(self, filename, job_name=None):
        if job_name is None:
            job_name = filename
        control = ('H{0}\nN{1}\nJ{2}\nP{3}\nl{4}\nU{4}\n').format(self.hostname, filename, job_name, self.user, self.df)
        payload = ('\x02{0} cfA000{1}\n').format(len(control), self.hostname)
        self.socket.send(payload)
        self.wait()
        self.socket.send(control)
        self.socket.send('\x00')
        self.wait()
        return

    def subcommand_receive_datafile(self, stream):
        stream.seek(0, 2)
        length = stream.tell()
        payload = ('\x03{0} {1}\n').format(length, self.df)
        self.socket.send(payload)
        self.wait()
        stream.seek(0, 0)
        x = 0
        while 1:
            data = stream.read(1024)
            if not data:
                break
            x += len(data)
            self.socket.send(data)

        self.socket.send('\x00')


if __name__ == '__main__':
    f = open('document.pdf', 'rb')
    lpr = LPR('crew.mormail.com', user='adam')
    lpr.connect()
    lpr.send_stream('cisps', 'test job', f, job_name='my awesome job')
    lpr.close()
    f.close()