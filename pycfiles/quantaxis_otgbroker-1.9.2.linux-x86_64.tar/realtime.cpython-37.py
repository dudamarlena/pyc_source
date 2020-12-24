# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/conda/lib/python3.7/site-packages/QA_OTGBroker/realtime.py
# Compiled at: 2019-11-10 13:49:23
# Size of source mod 2**32: 1286 bytes
from QAPUBSUB.producer import publisher_routing
from QUANTAXIS.QAEngine import QA_Thread
from QA_OTGBroker import on_pong, on_message, on_error, subscribe_quote, on_close, login, peek
import websocket, threading, click, time

class MARKET_SUBSCRIBER(QA_Thread):

    def __init__(self):
        super().__init__()
        self.ws = websocket.WebSocketApp('ws://openmd.shinnytech.com/t/md/front/mobile', on_pong=on_pong,
          on_message=(self.on_message),
          on_error=on_error,
          on_close=on_close)

        def _onopen(ws):

            def run():
                ws.send(subscribe_quote('SHFE.rb1910,DCE.j909'))
                ws.send(peek())

            threading.Thread(target=run, daemon=False).start()

        self.ws.on_open = _onopen
        threading.Thread(target=(self.ws.run_forever), name='market_websock',
          daemon=False).start()

    def on_message(self, message):
        print(message)
        self.ws.send(peek())

    def run(self):
        while True:
            time.sleep(1)


MARKET_SUBSCRIBER().run()