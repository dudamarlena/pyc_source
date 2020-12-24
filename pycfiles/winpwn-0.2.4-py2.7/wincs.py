# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winpwn\wincs.py
# Compiled at: 2020-04-17 22:05:27
import socket, threading, os, sys
from .winpwn import remote
from .asm import asm as ASM
from .asm import disasm as DISASM
from .misc import u32, p32, u64, p64, Latin1_encode, Latin1_decode, showbanner, showbuf, color
from .context import context

class wincs:

    def __init__(self, ip=None, port=512):
        self.wins = None
        self.winc = None
        if ip is None:
            self.wins = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.wins.bind((socket.gethostname(), port))
            self.wins.listen(5)
            threading.Thread(target=self.__winser_thread).start()
        else:
            self.winc = remote(ip, port)
        return

    def __winser_thread(self):
        try:
            while True:
                conn, client = self.wins.accept()
                threading.Thread(target=self.__handle_conn, args=(conn, client)).start()

        except KeyboardInterrupt:
            raise EOFError(color('[-]: Exited by CTRL+C', 'red'))

    def __handle_conn(self, conn, client):
        while 1:
            opcode = Latin1_decode(conn.recv(1))
            if opcode == '':
                showbanner(('wincs connection of {} closed').format(client), 'yellow', '[-]')
                return
            if opcode == '\x03':
                self.wins.close()
                showbanner('wincs server closed', 'yellow', '[-]')
                quit()
            else:
                arch = Latin1_decode(conn.recv(4))
                addr = u64(Latin1_decode(conn.recv(8)))
                length = u32(Latin1_decode(conn.recv(4)))
                code = Latin1_decode(conn.recv(length))
                is_asm = opcode == '\x01'
                if is_asm:
                    markstr = 'asm'
                else:
                    markstr = 'disasm'
                showbanner('wincs ' + markstr)
                showbuf(code)
                if is_asm:
                    rs = ASM(code, addr=addr, arch=arch)
                else:
                    rs = DISASM(code, addr=addr, arch=arch)
                showbanner('wincs ' + markstr + ' result')
                showbuf(rs)
                conn.send(Latin1_encode(p32(len(rs)) + rs))

    def __asm_disasm(self, code, addr, arch=None, is_asm=True):
        if arch is None:
            arch = context.arch
        if is_asm:
            markstr = 'asm'
            opcode = '\x01'
        else:
            markstr = 'disasm'
            opcode = '\x02'
        showbanner(markstr)
        showbuf(code)
        self.winc.write(opcode + arch.ljust(4, '\x00') + p64(addr) + p32(len(code)) + code)
        rs = self.winc.read(u32(self.winc.read(4)))
        showbanner(markstr + ' result')
        showbuf(rs)
        return rs

    def asm(self, asmcode, addr=0, arch=None):
        return self.__asm_disasm(code=asmcode, addr=addr, arch=arch, is_asm=True)

    def disasm(self, machinecode, addr=0, arch=None):
        return self.__asm_disasm(code=machinecode, addr=addr, arch=arch, is_asm=False)

    def close(self):
        self.winc.close()

    def close_server(self):
        self.winc.send(Latin1_encode('\x03'))