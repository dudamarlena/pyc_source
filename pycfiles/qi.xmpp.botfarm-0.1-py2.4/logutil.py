# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/xmpp/botfarm/logutil.py
# Compiled at: 2008-08-01 13:19:50
from twisted.python import log
from twisted.words.protocols.jabber import component
import sys, time, qi.xmpp.botfarm.config as config

class INFO:
    __module__ = __name__


class WARN:
    __module__ = __name__


class ERROR:
    __module__ = __name__


log.discardLogs()

class LogEvent:
    __module__ = __name__

    def __init__(self, category=INFO, ident='', msg='', log=True):
        self.category, self.ident, self.msg = category, ident, msg
        frame = sys._getframe(1)
        s = str(frame.f_locals.get('self', frame.f_code.co_filename))
        self.klass = s[s.find('.') + 1:s.find(' ')]
        self.method = frame.f_code.co_name
        self.args = frame.f_locals
        if log:
            if category == INFO and config.debugLevel < 3:
                return
            if category == WARN and config.debugLevel < 2:
                return
            if category == ERROR and config.debugLevel < 1:
                return
            self.log()

    def __str__(self):
        args = {}
        for key in self.args.keys():
            if key == 'self':
                args['self'] = 'instance'
                continue
            val = self.args[key]
            args[key] = val
            try:
                if len(val) > 128:
                    args[key] = 'Oversize arg'
            except:
                pass

        category = str(self.category).split('.')[1]
        return '%s :: %s :: %s\n' % (category, str(self.ident), self.msg)

    def log(self):
        log.msg(self)