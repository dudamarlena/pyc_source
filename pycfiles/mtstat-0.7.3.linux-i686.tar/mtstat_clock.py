# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mtstat/plugins/mtstat_clock.py
# Compiled at: 2006-12-12 18:59:17
import time
from mtstat.mtstat import mtstat

class mtstat_clock(mtstat):

    def __init__(self):
        self.name = 'clock'
        self.format = ('s', 14, 0)
        self.nick = ('date/time', )
        self.vars = self.nick

    def extract(self):
        pass

    def show(self):
        return time.strftime('%d-%m %H:%M:%S', time.gmtime())