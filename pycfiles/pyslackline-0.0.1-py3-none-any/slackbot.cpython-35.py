# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.5/site-packages/pyslackbot/slackbot.py
# Compiled at: 2016-05-01 18:09:35
# Size of source mod 2**32: 1904 bytes
from slackclient import SlackClient
import threading, time

class SlackBot(object):

    def __init__(self, bot_id, debug=False):
        self.sc = SlackClient(bot_id)
        self.user = ''
        self.connect = self.sc.rtm_connect()
        self.debug = debug
        self.threads = []
        t = threading.Thread(target=self.watch_message)
        self.threads.append(t)
        t.start()
        self.handlers = []

    def add_handler(self, msg, reply, run=None, con=True):
        handler = SlackHandler(msg, run, con)
        self.handlers.append(handler)

    def watch_message(self):
        if self.connect:
            self.sc.server.login_data['self']['id']
            while True:
                message = self.sc.rtm_read()
                if message and message[0]['type'] == 'message' and message[0]['user'] != self.user:
                    text = message[0]['text']
                    if self.debug:
                        print('Message - ' + text)
                    self.parse_message(text, message[0]['channel'])
                time.sleep(1)

    def parse_message(self, message, channel):
        for handler in self.handlers:
            if handler.con:
                if handler.message in message:
                    if handler.run != None:
                        if self.debug:
                            print('Excuting - ' + str(handler.run))
                        try:
                            handler.run()
                        except:
                            print('Exception during handler function')

                        self.sc.rtm_send_message(channel, message)
                    elif handler.message == message:
                        handler.run()


class SlackHandler(object):

    def __init__(self, message, run, con):
        self.message = message
        self.run = run
        self.con = con