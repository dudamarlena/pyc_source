# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sch/prj/pytigon/pytigon/prj/_schtools/schcommander/consumers.py
# Compiled at: 2020-01-02 14:18:58
# Size of source mod 2**32: 2416 bytes
import os, sys, datetime, json, asyncio
from channels.consumer import AsyncConsumer, SyncConsumer
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer, JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.generic.http import AsyncHttpConsumer
import select, time
from threading import Thread
import subprocess, struct
try:
    import pty, fcntl, termios
except:
    pass

from pytigon_lib.schtools.tools import get_executable

def read_and_forward_pty_output(consumer):
    max_read_bytes = 20480
    while not consumer.exit:
        time.sleep(0.01)
        if consumer.fd:
            timeout_sec = 1
            data_ready, _, _ = select.select([consumer.fd], [], [], timeout_sec)
            if data_ready:
                output = os.read(consumer.fd, max_read_bytes).decode()
                if output:
                    consumer.send(text_data=output)

    print('Shell closed')


class ShellConsumer(WebsocketConsumer):

    def set_winsize(self, fd, row, col, xpix=0, ypix=0):
        winsize = struct.pack('HHHH', row, col, xpix, ypix)
        fcntl.ioctl(self.fd, termios.TIOCSWINSZ, winsize)

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            x = json.loads(text_data)
            if 'input' in x:
                if self.fd:
                    os.write(self.fd, x['input'].encode('utf-8'))
            if 'resize' in x:
                size = x['resize']
                if self.fd:
                    self.set_winsize(self.fd, size['rows'], size['cols'])

    def connect(self):
        print('Connecting.......')
        self.exit = False
        self.fd = None
        self.child_pid = None
        self.accept()
        child_pid, fd = pty.fork()
        if child_pid == 0:
            env2 = os.environ.copy()
            env2['TERM'] = 'xterm'
            subprocess.run([get_executable(), '-m', 'xonsh'], env=env2)
        else:
            self.fd = fd
            self.child_pid = child_pid
            self.thread = Thread(target=read_and_forward_pty_output, args=(self,))
            self.thread.start()

    def disconnect(self, close_code):
        print('Disconnect.......')
        self.exit = True
        os.write(self.fd, b'exit\n')