# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/bcsdk/impl/impl.py
# Compiled at: 2019-12-09 06:09:45
# Size of source mod 2**32: 1243 bytes
import os, flask, logging, socketio, requests
from bcsdk.impl.sio import sio, set_handler
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = flask.Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    print('Shutting down....')
    shutdown_function = flask.request.environ.get('werkzeug.server.shutdown')
    if shutdown_function is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_function()
    sio.emit('status', {'fill':'red',  'shape':'dot',  'text':'Container server down'})
    return 'Server shutting down...'


def _start_server(handler):
    set_handler(handler)
    port = int(os.environ.get('PORT', '3000'))
    print('Starting server on port ' + str(port))
    app.run(host='0.0.0.0', port=port, threaded=True, debug=False)


def _stop_server():
    print('stopping server')
    sio.emit('status', {'fill':'orange',  'shape':'dot',  'text':'Shutting down'})
    port = int(os.environ.get('PORT', '3000'))
    requests.post('http://0.0.0.0:{}/shutdown'.format(port))