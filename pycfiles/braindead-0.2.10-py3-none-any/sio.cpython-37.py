# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.7/site-packages/bcsdk/impl/sio.py
# Compiled at: 2019-12-09 06:01:39
# Size of source mod 2**32: 690 bytes
import socketio
sio = socketio.Server(async_mode='threading')
current_handler = None

def set_handler(handler):
    global current_handler
    current_handler = handler


@sio.event
def connect(sid, environ):
    print('Edgebox connected')
    sio.emit('status', {'fill':'green',  'shape':'dot',  'text':'Edgebox connected'})


@sio.event
def disconnect(sid):
    print('Disconnected')
    current_handler.on_destroy()


@sio.event
def configuration(sid, data):
    print('Received configuration: {}'.format(data))
    current_handler.on_init(data)


@sio.event
def msg(sid, data):
    print('Received message ' + str(data))
    current_handler.on_message(data)