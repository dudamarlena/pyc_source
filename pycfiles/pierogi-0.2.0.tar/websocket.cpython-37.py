# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/manu/Documents/pierogi/pierogi/utils/websocket.py
# Compiled at: 2019-07-18 04:55:37
# Size of source mod 2**32: 4889 bytes
import threading as _threading, asyncio as _asyncio, websockets as _websockets

class WebSocketServer:
    __doc__ = '\n    Web Socket Server\n\n    Best way to use:\n    ```\n    with WebSocketServer() as web_socket_server:\n        web_socket_server.send("message 1")\n        # Your stuff here\n        web_socket_server.send("message 2")\n        # Your stuff here\n        web_socket_server.send("message 2")\n\n        # The server will be close (and so data not retrievable any more)\n          after the following input\n        input("Hit enter to close the websocket server.")\n    ```\n\n    If you want to play around in the console or if you don\'t want to use the\n    `with` statement, you can do that:\n\n    ```\n    web_socket_server = WebSocketServer()\n    web_socket_server.start()\n\n    web_socket_server.send("message 1")\n    # Your stuff here\n    web_socket_server.send("message 2")\n    # Your stuff here\n    web_socket_server.send("message 2")\n\n    web_socket_server.stop()\n    ```\n\n    WARNING: In this case, don\'t forget to call the stop method at the end,\n             else your program/console will has trouble to close\n\n    To test this web socket server, you can use websocket_client.html in your\n    web browser. This webpage has to be loaded AFTER the server is started and\n    BEFORE the server is closed. Note that messages sent by the server between\n    the server start and this webpage connection WON\'T be lost :) !\n    '
    _WebSocketServer__DEFAULT_ADRESS = 'localhost'
    _WebSocketServer__DEFAULT_ADRESS: str
    _WebSocketServer__DEFAULT_PORT = 9559
    _WebSocketServer__DEFAULT_PORT: int

    def __init__(self, adress: str=_WebSocketServer__DEFAULT_ADRESS, port: int=_WebSocketServer__DEFAULT_PORT):
        """Initialization

        Positional arguments:
            adress - The adress
            port   - The port
        """
        self._WebSocketServer__adress = adress
        self._WebSocketServer__port = port
        self._WebSocketServer__clients = set()
        self._WebSocketServer__started = False

    async def __handler(self, client: _websockets.protocol.WebSocketCommonProtocol, _) -> None:
        try:
            for element in self._WebSocketServer__sent:
                await client.send(element)

        except _websockets.ConnectionClosed:
            pass

        self._WebSocketServer__clients.add(client)
        has_to_continue = True
        while has_to_continue:
            outgoing = _asyncio.ensure_future(self._WebSocketServer__inputs.get())
            dp_ = await _asyncio.wait([outgoing, self._WebSocketServer__fut_interrupt], return_when=(_asyncio.FIRST_COMPLETED))
            done, pending = dp_
            if outgoing in pending:
                outgoing.cancel()
                try:
                    await outgoing
                except _asyncio.CancelledError:
                    pass

            if outgoing in done:
                to_send = outgoing.result()
                self._WebSocketServer__sent.append(to_send)
                lost_clients = set()
                for client in self._WebSocketServer__clients:
                    try:
                        await client.send(to_send)
                    except _websockets.ConnectionClosed:
                        lost_clients.add(client)

                if len(lost_clients) != 0:
                    self._WebSocketServer__clients -= lost_clients
            if self._WebSocketServer__fut_interrupt in done:
                has_to_continue = False

    def start(self) -> None:
        """Start"""
        if self._WebSocketServer__started:
            return
        self._WebSocketServer__sent = []
        self._WebSocketServer__loop = _asyncio.get_event_loop()
        self._WebSocketServer__inputs = _asyncio.Queue()
        self._WebSocketServer__fut_interrupt = self._WebSocketServer__loop.create_future()
        self._WebSocketServer__serve = _websockets.serve(self._WebSocketServer__handler, self._WebSocketServer__adress, self._WebSocketServer__port)
        self._WebSocketServer__loop.run_until_complete(self._WebSocketServer__serve)
        self._WebSocketServer__thread = _threading.Thread(target=(self._WebSocketServer__loop.run_forever), name='server')
        self._WebSocketServer__thread.start()
        self._WebSocketServer__started = True

    def stop(self) -> None:
        """Stop"""
        if not self._WebSocketServer__started:
            return
        self._WebSocketServer__loop.call_soon_threadsafe(self._WebSocketServer__fut_interrupt.set_result, None)
        self._WebSocketServer__serve.ws_server.close()
        self._WebSocketServer__loop.stop()
        self._WebSocketServer__thread.join()
        self._WebSocketServer__started = False

    def send(self, message: str) -> None:
        """
        Send a message

        Positional argument:
        message - The message to send
        """
        if not self._WebSocketServer__started:
            raise RuntimeError('Server not started. Please call `start`')
        self._WebSocketServer__loop.call_soon_threadsafe(self._WebSocketServer__inputs.put_nowait, message)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *_):
        self.stop()