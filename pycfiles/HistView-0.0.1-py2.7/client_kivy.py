# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-x86_64/egg/HistView/client_kivy.py
# Compiled at: 2015-11-11 16:06:45
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
import pickle

class MyKivyClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        self.factory._app.print_message('WebSocket connection open.')
        self.factory._proto = self

    def onMessage(self, payload, isBinary):
        if isBinary:
            self.factory._app.print_message(('Binary message received: {0} bytes').format(len(payload)))
        else:
            self.factory._app.print_message(('Got from server: {}').format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        self.factory._app.print_message(('WebSocket connection closed: {0}').format(reason))
        self.factory._proto = None
        return


class MyKivyClientFactory(WebSocketClientFactory):
    protocol = MyKivyClientProtocol
    _msg_protocols = ['dist_pickle']

    def __init__(self, url, app):
        WebSocketClientFactory.__init__(self, url, protocols=self._msg_protocols)
        self._app = app
        self._proto = None
        return


from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from twisted.internet import reactor
import API.HistologyAPI

class KivyClientApp(App):

    def build(self):
        root = self.setup_gui()
        self.connect_to_server()
        return root

    def setup_gui(self):
        """
        Create a vertical oriented boxlayout that contains two widgets:
        1) a label in which we show text sent/received
        2) a textinput where you can enter text
           to the server.
        """
        self.label = Label(text='Connecting...\n')
        self.textbox = TextInput(size_hint_y=0.1, multiline=False)
        self.textbox.bind(on_text_validate=self.send_message)
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.textbox)
        return self.layout

    def connect_to_server(self):
        """
        Connect to the echoing websocket server.
        """
        self._factory = MyKivyClientFactory('ws://localhost:9000', self)
        reactor.connectTCP('127.0.0.1', 9000, self._factory)

    def send_message(self, *args):
        """
        Send the text entered that was entered in the texbox widget.
        """
        msg = API.TestString()
        msg.input = self.textbox.text
        proto = self._factory._proto
        if msg and proto:
            p = pickle.dumps(msg, protocol=2)
            proto.sendMessage(p, isBinary=True)
            self.print_message(('Sent to server: {}').format(self.textbox.text))
            self.textbox.text = ''

    def print_message(self, msg):
        self.label.text += msg + '\n'


if __name__ == '__main__':
    import sys
    from twisted.python import log
    log.startLogging(sys.stdout)
    KivyClientApp().run()