# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\socket_says\socket_says.py
# Compiled at: 2020-04-19 23:39:16
# Size of source mod 2**32: 3106 bytes
from abc import ABC
import atexit
from socket import socket, AF_INET, SOCK_STREAM
from ipaddress import ip_address
from .custom_errors import BadPortError, BadAddressError

class SocketSays(ABC):

    def __init__(self, address='127.0.0.1', port=80):
        self.address = address
        self.port = port
        self.text = 'Hello'
        self.socket = self.establish_socket()
        atexit.register(self.close_socket)

    def __len__(self):
        return len(self.text)

    def __str__(self):
        return "You are telling {} on port {} '{}'".format(self.address, self.port, self.text)

    def __repr__(self):
        return '<SocketSays({},{},{})>'.format(self.address, self.port, self.text)

    def says(self, msg_text='Hello', *, special=None):
        """ Creates SocketSays' ability to speak on the socket"""
        self.text = msg_text
        for line in self.text.splitlines():
            self.volley(self.format_text(line + '\n', special))

    def listens(self, multiple=4500):
        """ Creates SocketSays' ability to receive on the socket"""
        try:
            self.socket.settimeout(1.5)
            print(self.socket.recv(2048 * multiple).decode())
        except:
            pass

    def volley(self, text: str):
        if self.socket:
            self.socket.send(text)
        else:
            print('There is no connection')

    def close_socket(self):
        try:
            self.socket.close()
        except AttributeError:
            pass

    def format_text(self, text='', special=None):
        if special:
            pass
        return text.encode()

    def establish_socket--- This code section failed: ---

 L.  69         0  LOAD_FAST                'old_socket'
                2  POP_JUMP_IF_FALSE    12  'to 12'

 L.  70         4  LOAD_FAST                'self'
                6  LOAD_METHOD              close_socket
                8  CALL_METHOD_0         0  ''
               10  POP_TOP          
             12_0  COME_FROM             2  '2'

 L.  71        12  LOAD_GLOBAL              socket
               14  LOAD_GLOBAL              AF_INET
               16  LOAD_GLOBAL              SOCK_STREAM
               18  CALL_FUNCTION_2       2  ''
               20  STORE_FAST               'new_socket'

 L.  72        22  SETUP_FINALLY        52  'to 52'

 L.  73        24  LOAD_FAST                'new_socket'
               26  LOAD_METHOD              connect
               28  LOAD_GLOBAL              str
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                address
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                port
               40  BUILD_TUPLE_2         2 
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L.  74        46  LOAD_FAST                'new_socket'
               48  POP_BLOCK        
               50  RETURN_VALUE     
             52_0  COME_FROM_FINALLY    22  '22'

 L.  75        52  DUP_TOP          
               54  LOAD_GLOBAL              ConnectionRefusedError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    92  'to 92'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.  76        66  LOAD_GLOBAL              print
               68  LOAD_STR                 "I'm sorry. The connection was refused to {} port {}"
               70  LOAD_METHOD              format
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                address
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                port
               80  CALL_METHOD_2         2  ''
               82  CALL_FUNCTION_1       1  ''
               84  POP_TOP          

 L.  77        86  POP_EXCEPT       
               88  LOAD_CONST               None
               90  RETURN_VALUE     
             92_0  COME_FROM            58  '58'
               92  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 62

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, val):
        try:
            self._address = ip_address(val)
        except ValueError as e:
            try:
                raise BadAddressError(e)
            finally:
                e = None
                del e

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, val):
        try:
            self._port = int(val)
        except ValueError as e:
            try:
                raise BadPortError(e)
            finally:
                e = None
                del e

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val):
        self._text = val