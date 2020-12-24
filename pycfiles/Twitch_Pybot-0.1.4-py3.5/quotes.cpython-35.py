# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pybot/features/quotes.py
# Compiled at: 2016-07-13 16:56:07
# Size of source mod 2**32: 1222 bytes
from pybot.pybotextra import *
import pybot.globals as globals, random
from pybot.data import *

class Quotes:

    def __init__(self, conn):
        self.conn = conn
        conn.addHook(self.hook)

    def hook(self, con, msg, event):
        if event == 'user_privmsg':
            name = msg.replace(':', '').split('!')[0].replace('\n\r', '')
            text = msg.split('PRIVMSG')[1].replace('%s :' % con.channel, '')
            if checkIfCommand(text, '!quote') and toBool(globals.settings.config['features']['quotes']):
                quote = text.split('quote', 1)
                if len(quote) > 1 and quote[1] != '':
                    self.addQuote(name, quote[1])
                    con.msg('Quote as been added.')
        elif self.getRandomQuote():
            con.msg(self.getRandomQuote())

    def addQuote(self, name, text):
        globals.data.quotes.append('"' + text + '" - ' + name)
        globals.data.save()

    def getRandomQuote(self):
        if len(globals.data.quotes) > 0:
            return globals.data.quotes[random.randint(0, len(globals.data.quotes) - 1)]
        return False