# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\Joseph\PycharmProjects\pyformulas\_formulas\net\Stream.py
# Compiled at: 2018-05-21 18:26:46
# Size of source mod 2**32: 3929 bytes
import pyformulas as pf

class Stream:

    def __init__(self, port, address=None, is_server=None, max_connections=5):
        self._connections = []
        if is_server or address is None:
            self._isserver = True
            self._make_server(port, bind_address=('' if address is None else address), max_connections=max_connections)
        else:
            self._isserver = False
            self._make_client(port, address)

    def on_receive(self, conn, buffer):
        pass

    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        pass

    def shutdown(self):
        if self._isserver:
            try:
                self._serversocket.close()
            except:
                pass

        for conn in self._connections:
            conn.disconnect()

    def _make_server(self, port, bind_address, max_connections):
        import socket
        self._serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._serversocket.bind((bind_address, port))
        self._serversocket.listen(max_connections)
        for i in range(max_connections):
            pf.thread(self._server_accept)

    def _server_accept(self):
        try:
            socket, address = self._serversocket.accept()
        except:
            return
        else:
            connection = self._Connection(self, socket)
            self._connections.append(connection)

    def _make_client(self, port, address):
        import socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((address, port))
        connection = self._Connection(self, client_socket)
        self._connections.append(connection)

    class _Connection:

        def __init__(self, stream, socket):
            from select import select
            from time import sleep
            self._select = select
            self._sleep = sleep
            self._stream = stream
            self.socket = socket
            self._disconnected = False
            pf.thread(self._recv_loop)
            self._stream.on_connect(self)

        def disconnect(self):
            if self._disconnected:
                return
            self._disconnected = True
            try:
                self.socket.close()
            except:
                pass

            self._stream._connections.remove(self)
            if self._stream._isserver:
                if self._stream._serversocket.fileno() != -1:
                    pf.thread(self._stream._server_accept)
            self._stream.on_disconnect(self)

        def send(self, bytes):
            try:
                self.socket.send(bytes)
            except:
                self.disconnect()

        def _recv_loop(self):
            from select import select
            from time import sleep
            while self.socket.fileno() != -1:
                try:
                    if len(select([self.socket], [], [], 0)[0]) == 1:
                        break
                except ValueError:
                    self.disconnect()
                    return
                else:
                    if self._disconnected:
                        return
                    sleep(1e-09)

            while True:
                try:
                    buffer = self.socket.recv(4096)
                except:
                    self.disconnect()
                    return

                if len(buffer) > 0:
                    pf.thread(lambda : self._stream.on_receive(self, buffer))
                else:
                    self.disconnect()
                    return