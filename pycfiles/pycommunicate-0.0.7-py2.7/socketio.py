# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pycommunicate\server\app\socketio.py
# Compiled at: 2016-06-11 08:13:17
import flask_socketio, eventlet

class SocketIOContainer:
    """
    The socketio interface. THIS SHOULD BE THE MAIN ENTRY POINT!!
    """

    def __init__(self, app):
        """

        :type app: pycommunicate.server.app.communicate.CommunicateApp
        """
        self.socketio = flask_socketio.SocketIO(app.flask)
        self.send_queue = eventlet.queue.Queue()
        self.app = app
        self.awaited_responses = {}
        self.event_dispatchers = {}
        self.create_handlers()

    def on_connect(self, request_id):
        user = self.app.user_tracker.users[self.app.user_tracker.requests[request_id]]
        if user.socket_connected:
            return
        user.socket_connect()
        flask_socketio.join_room(request_id)

    def create_handlers(self):

        @self.socketio.on('setup')
        def connect(request_id):
            self.on_connect(request_id)

        @self.socketio.on('teardown')
        def teardown(request_id):
            self.on_teardown(request_id)

        @self.socketio.on('response')
        def response(response_data, tag):
            self.awaited_responses[tag].put(response_data)

        @self.socketio.on('event')
        def event(event_id):
            self.app.green_pool.spawn_n(self.event_dispatchers[event_id])

    def send(self, event_id, room, args, tag=''):
        thing = (room, event_id, list(args) + [tag] if tag is not '' else list(args))
        if tag != '':
            self.awaited_responses[tag] = eventlet.queue.Queue()
        self.send_queue.put(thing)

    def received_response(self, tag):
        return not self.awaited_responses[tag].empty()

    def await_response(self, tag):
        return_value = self.awaited_responses[tag].get()
        del self.awaited_responses[tag]
        return return_value

    def send_daemon(self):
        while True:
            data = self.send_queue.get()
            self.socketio.emit(data[1], data[2], room=data[0])

    def start_handlers(self, pool):
        pool.spawn_n(self.send_daemon)

    def on_teardown(self, request_id):
        user = self.app.user_tracker.users[self.app.user_tracker.requests[request_id]]
        user.socket_connected = False