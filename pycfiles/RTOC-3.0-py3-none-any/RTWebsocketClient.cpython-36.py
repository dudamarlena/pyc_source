# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\RTLogger\RTWebsocketClient.py
# Compiled at: 2020-01-06 18:23:37
# Size of source mod 2**32: 12044 bytes
import os, traceback, json
from threading import Thread
import time, base64, psutil
from functools import partial
import ssl
try:
    from . import RTWebsocket
except ImportError:
    import RTWebsocket

import websocket
try:
    from PyQt5.QtCore import QCoreApplication
    translate = QCoreApplication.translate
except ImportError:

    def translate(id, text):
        return text


def _(text):
    return translate('websocket', text)


import logging as log
log.basicConfig(level=(log.INFO))
logging = log.getLogger(__name__)
HOST_WHITELIST = [
 '127.0.0.1', 'localhost']
DEBUG = False

def PRINTDEBUG(typ=None, element=None):
    if typ == 'UNKNOWN':
        logging.warning('Received: {}'.format(typ))
        logging.warning(element)
    else:
        if typ == 'Error':
            logging.error('Received: {}'.format(typ))
            logging.error(element)
        else:
            logging.info('Received: {}'.format(typ))
            logging.info(element)


class RTWebsocketClient:
    __doc__ = '\n    This class contains all Websocket-specific functions for RTLogger-Clients\n    '

    def __init__(self, host=None, port=5050, password=None, usessl=False):
        if password is not None:
            self._RTWebsocketClient__password = RTWebsocket.hashPassword(password)
            self._RTWebsocketClient__password_full = RTWebsocket.hashPassword(password, True)
        else:
            self._RTWebsocketClient__password = None
            self._RTWebsocketClient__password_full = None
        self.run = False
        self.ws = None
        self.port = port
        self.host = host
        self.usessl = usessl
        if DEBUG:
            self.handle_authorize = partial(PRINTDEBUG, 'Authorize')
            self.handle_pluginList = partial(PRINTDEBUG, 'PluginList')
            self.handle_signalList = partial(PRINTDEBUG, 'SignalList')
            self.handle_plugin = partial(PRINTDEBUG, 'Plugin')
            self.handle_latest = partial(PRINTDEBUG, 'Latest')
            self.handle_automation = partial(PRINTDEBUG, 'Automation')
            self.handle_client = partial(PRINTDEBUG, 'Client')
            self.handle_events = partial(PRINTDEBUG, 'Events')
            self.handle_signal = partial(PRINTDEBUG, 'Signal')
            self.handle_userAction = partial(PRINTDEBUG, 'UserAction')
            self.handle_logger = partial(PRINTDEBUG, 'Logger')
            self.handle_event = partial(PRINTDEBUG, 'Event')
            self.handle_session = partial(PRINTDEBUG, 'Event')
            self.handle_signals = partial(PRINTDEBUG, 'Signals')
            self.handle_RTOCError = partial(PRINTDEBUG, 'Error')
            self.handle_unknown = partial(PRINTDEBUG, 'UNKNOWN')
            self.on_message = None
            self.on_error = partial(PRINTDEBUG, 'Error')
            self.on_close = partial(PRINTDEBUG, 'Close')
            self.on_open = partial(PRINTDEBUG, 'Open')
        else:
            self.handle_authorize = None
            self.handle_pluginList = None
            self.handle_signalList = None
            self.handle_plugin = None
            self.handle_latest = None
            self.handle_automation = None
            self.handle_client = None
            self.handle_events = None
            self.handle_signal = None
            self.handle_userAction = None
            self.handle_logger = None
            self.handle_event = None
            self.handle_session = None
            self.handle_signals = None
            self.handle_RTOCError = None
            self.on_message = None
            self.on_error = None
            self.on_close = None
            self.on_open = None
            self.handle_unknown = None
        if type(self.host) == str:
            if type != '':
                self.connect(host)

    def connect(self, host=None, port=None, password=None, usessl=None):
        if host != None:
            if type(host) == str:
                self.host = host
            else:
                if password != None:
                    if type(password) == str:
                        self._RTWebsocketClient__password = RTWebsocket.hashPassword(password)
                        self._RTWebsocketClient__password_full = RTWebsocket.hashPassword(password, True)
                if port != None:
                    if type(port) == int:
                        self.port = port
                if usessl != None:
                    if type(usessl) == bool:
                        self.usessl = usessl
        else:
            if self._RTWebsocketClient__password == None:
                logging.warning('Websockets are used without encryption!')
            else:
                if self.usessl:
                    prefix = 'wss://'
                else:
                    prefix = 'ws://'
            link = prefix + self.host + ':' + str(self.port)
            print('Connecting with {}'.format(link))
            websocket.enableTrace(False)
            self.ws = websocket.WebSocketApp(link, on_message=(self.handle_message),
              on_error=(self.handle_error),
              on_close=(self.handle_close))
            self.ws.on_open = self.handle_open
            if self.usessl:
                sslopt = {'sslopt': {'cert_reqs': ssl.CERT_NONE}}
            else:
                sslopt = {}
        self.runner = Thread(target=(self.ws.run_forever), kwargs=sslopt)
        self.runner.daemon = True
        self.runner.start()

    def disconnect(self):
        if self.ws == None:
            return
        self.run = False
        self.ws.keep_running = False
        self.runner = None
        self.ws = None

    def handle_error(self, error):
        if self.on_error != None:
            self.on_error(error)

    def handle_close(self):
        if self.on_close != None:
            self.on_close()

    def handle_open(self):
        self.run = True
        if self._RTWebsocketClient__password != None:
            self.send(authorize=(self._RTWebsocketClient__password_full.decode()))
        else:
            self.send(authorize=True)
        if self.on_open != None:
            self.on_open()

    def handle_message(self, message):
        try:
            if self.host not in HOST_WHITELIST:
                msg = RTWebsocket.recv(message, self._RTWebsocketClient__password)
            else:
                msg = json.loads(message)
            if msg == None:
                logging.error('Could not parse received message')
                if self.handle_RTOCError != None:
                    self.handle_RTOCError()
                return
            if 'authorized' in msg.keys():
                if self.handle_authorize != None:
                    self.handle_authorize(msg['authorized'])
                    msg.pop('authorized')
            if 'pluginList' in msg.keys():
                if self.handle_pluginList != None:
                    self.handle_pluginList(msg['pluginList'])
                    msg.pop('pluginList')
            if 'signalList' in msg.keys():
                if self.handle_signalList != None:
                    self.handle_signalList(msg['signalList'])
                    msg.pop('signalList')
            if 'plugin' in msg.keys() and self.handle_plugin != None:
                self.handle_plugin(msg['plugin'])
                msg.pop('plugin')
            if 'latest' in msg.keys():
                if self.handle_latest != None:
                    self.handle_latest(msg['latest'])
                    msg.pop('latest')
            if 'automation' in msg.keys():
                if self.handle_automation != None:
                    self.handle_automation(msg['automation'])
                    msg.pop('automation')
            if 'client' in msg.keys():
                if self.handle_client != None:
                    self.handle_client(msg['client'])
                    msg.pop('client')
            if 'events' in msg.keys():
                if self.handle_events != None:
                    self.handle_events(msg['events'])
                    msg.pop('events')
            if 'signal' in msg.keys():
                if self.handle_signal != None:
                    self.handle_signal(msg['signal'])
                    msg.pop('signal')
            if 'userAction' in msg.keys():
                if self.handle_userAction != None:
                    self.handle_userAction(msg['userAction'])
                    msg.pop('userAction')
            if 'logger' in msg.keys():
                if self.handle_logger != None:
                    self.handle_logger(msg['logger'])
                    msg.pop('logger')
            if 'event' in msg.keys():
                if self.handle_event != None:
                    self.handle_event(msg['event'])
                    msg.pop('event')
            if 'signals' in msg.keys():
                if self.handle_signals != None:
                    self.handle_signals(msg['signals'])
                    msg.pop('signals')
            if 'error' in msg.keys():
                if msg['error'] == True:
                    logging.error('Some error occured at the host')
                    if self.handle_RTOCError != None:
                        self.handle_RTOCError()
                msg.pop('error')
            if 'session' in msg.keys():
                if self.handle_session != None:
                    self.handle_session(msg['session'])
            if msg != {}:
                if DEBUG:
                    logging.warning('Unhandled data:\n{}'.format(msg))
                if self.handle_unknown != None:
                    self.handle_unknown(msg)
            if self.on_message != None:
                self.on_message(msg)
        except RTWebsocket.WrongPasswordError:
            logging.info('Wrong password.')
            if self.handle_RTOCError:
                self.handle_RTOCError()
        except RTWebsocket.NoPasswordProtectionError:
            logging.info('No password protection.')
            if self.handle_RTOCError:
                self.handle_RTOCError()
        except KeyboardInterrupt:
            logging.info('websocket connection stopped by user input.')
            self.disconnect()
        except Exception:
            tb = traceback.format_exc()
            logging.debug(tb)
            print(tb)
            logging.warning('Error in websocket-Connection')

    def send(self, **kwargs):
        self.sendWebsocketJSON(kwargs)

    def sendWebsocketJSON(self, message):
        if self.ws == None:
            return
        else:
            if DEBUG:
                print('Send\n{}'.format(message))
            if self.host not in HOST_WHITELIST:
                if self._RTWebsocketClient__password != None:
                    msg = RTWebsocket.send(message, self._RTWebsocketClient__password)
            msg = json.dumps(message)
        self.ws.send(msg)


if __name__ == '__main__':
    DEBUG = True
    test = RTWebsocketClient()
    try:
        hostname = input('Enter a hostname (localhost): ')
        if hostname == '':
            hostname = 'localhost'
        port = None
        while port == None:
            port = input('Enter a port (5050): ')
            if port == '':
                port = 5050
            else:
                try:
                    port = int(port)
                except:
                    port = None

        password = input('Enter password (optional): ')
        if password == '':
            password = None
        usessl = input('Is SSL-encrypted? (y/N)')
        if usessl != 'y':
            usessl = False
        else:
            usessl = True
        test.connect(hostname, port=port, password=password, usessl=usessl)
        msg = None
        print('Now you can send requests')
        while msg != 'exit':
            msg = input()
            if msg == 'exit':
                pass
            else:
                try:
                    a = json.loads(msg)
                    test.sendWebsocketJSON(a)
                except Exception as e:
                    print('Wrong input: {}'.format(e))
                    msg = ''

        print('Disconnecting from RTOC-Server')
        test.disconnect()
        print('Connection closed')
    except KeyboardInterrupt:
        test.disconnect()