# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/manu/Documents/pierogi/pierogi/pierogi.py
# Compiled at: 2019-07-21 11:30:09
# Size of source mod 2**32: 2534 bytes
import utils.websocket as _WebSocketServer
import webbrowser as _webbrowser, os as _os
import os.path as _path
import json as _json
_LOC = _path.realpath(_path.join(_os.getcwd(), _path.dirname(__file__)))
_WEB_APP_PATH = _os.path.join(_LOC, 'webapp', 'pierogi.html')

class Pierogi:
    __doc__ = '\n    Plot your training data on your web browser.\n\n    Best way to use:\n    ```\n    with Pierogi() as pierogi:\n        # Your stuff here\n        pierogi.append_training_loss(2.1)\n        # Your stuff here\n        web_socket_server.append_training_loss(1.4)\n        # Your stuff here\n        web_socket_server.append_training_loss(0.9)\n\n        # Pierogi will be close (and so data not retrievable any more on the\n        # web browser) after the following input\n        input("Hit enter to stop Pierogi.")\n    ```\n\n    If you want to play around in the console or if you don\'t want to use the\n    `with` statement, you can do that:\n\n    ```\n    pierogi = Pierogi()\n    pierogi.start()\n\n    # Your stuff here\n    pierogi.append_training_loss(2.1)\n    # Your stuff here\n    web_socket_server.append_training_loss(1.4)\n    # Your stuff here\n    web_socket_server.append_training_loss(0.9)\n\n    pierogi.stop()\n    ```\n\n    WARNING: In this case, don\'t forget to call the stop method at the end,\n             else your program/console will has trouble to close\n\n    '

    def __init__(self):
        """Initialization"""
        self._Pierogi__web_socket_server = _WebSocketServer()

    def start(self):
        """Start and open the web browser"""
        self._Pierogi__web_socket_server.start()
        _webbrowser.open(_WEB_APP_PATH)

    def stop(self):
        """Stop"""
        self._Pierogi__web_socket_server.stop()

    def configure(self, nb_epochs=None, nb_batches_per_epoch=None):
        to_send = {}
        if nb_epochs:
            to_send['nb_epochs'] = nb_epochs
        if nb_batches_per_epoch:
            to_send['nb_batches_per_epoch'] = nb_batches_per_epoch
        self._Pierogi__web_socket_server.send(_json.dumps(to_send))

    def plot_loss(self, epoch, batch, loss, type='train'):
        """Append the train loss

        Positional argument:
        loss - The train loss

        Keyword argument:
        type - Has to be "train" or "validation"
        """
        to_send = {'epoch': epoch, 'batch': batch, f"{type}_loss": loss}
        self._Pierogi__web_socket_server.send(_json.dumps(to_send))

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *_):
        self.stop()