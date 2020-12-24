# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ploader/server.py
# Compiled at: 2014-01-14 07:49:27
# Size of source mod 2**32: 1804 bytes
from ploader.commands import interface_commands
from ploader.dlc_handler import dlc_to_links
import asyncore, socket, shlex, select, ploader.utils as utils

class Client(asyncore.dispatcher_with_send):

    def __init__(self, sock, callback):
        super().__init__(sock)
        self.sock = sock
        self.callback = callback
        self.cur_command = None
        self.command_string = '/'.join(interface_commands)
        self.send(('Welcome (try %s)\n' % self.command_string).encode(encoding='UTF-8'))
        return

    def handle_read(self):
        data = self.recv(8192)
        answ = "I don't know what to do... (try %s)" % self.command_string
        if data:
            inp = data.decode(encoding='UTF-8').rstrip('\n')
            if self.cur_command == None:
                if inp in interface_commands.keys():
                    self.cur_command = interface_commands[inp]()
            if self.cur_command != None:
                next_state, info = self.cur_command.execute(inp)
                if next_state == 'proceed':
                    answ = info
                else:
                    if next_state == 'error':
                        answ = info
                        self.cur_command = None
                    elif next_state == 'return':
                        answ = self.callback({info: self.cur_command.execute(inp)})
                        self.cur_command = None
        self.send(('%s\n' % answ).encode(encoding='UTF-8'))
        return


class Server(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.callback = None
        return

    def handle_accepted(self, sock, addr):
        print('Incoming connection from %s' % repr(addr))
        client = Client(sock, self.callback)

    def set_callback(self, callback):
        self.callback = callback