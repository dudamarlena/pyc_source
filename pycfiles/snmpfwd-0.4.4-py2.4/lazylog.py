# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpfwd/lazylog.py
# Compiled at: 2018-03-07 06:10:36
from pysnmp.proto.api import v2c

class LazyLogString(object):
    __module__ = __name__
    ALIASES = {}
    GROUPINGS = []
    FORMATTERS = {}

    def __init__(self, *contexts):
        self._ctx = {}
        for ctx in contexts:
            self._ctx.update(ctx)

        self._dirty = bool(contexts)
        self._logMsg = ''

    def __str__(self):
        if self._dirty:
            self._dirty = False
            ctx = self._ctx
            self._logMsg = ''
            for grouping in self.GROUPINGS:
                for key in grouping:
                    if key not in ctx:
                        continue
                    val = ctx[key]
                    if key in self.FORMATTERS:
                        val = self.FORMATTERS[key](val)
                    elif isinstance(val, int):
                        val = str(val)
                    elif val:
                        val = v2c.OctetString(val).prettyPrint()
                    if key in self.ALIASES:
                        key = self.ALIASES[key]
                    self._logMsg += '%s=%s ' % (key, val or '<nil>')

        return self._logMsg

    def update(self, ctx):
        self._ctx.update(ctx)
        self._dirty = True

    @staticmethod
    def prettyVarBinds(pdu):
        if pdu:
            logMsg = pdu.__class__.__name__ + '#'
            for (oid, val) in v2c.apiPDU.getVarBinds(pdu):
                val = val.prettyPrint()
                if len(val) > 32:
                    val = val[:32] + '...'
                if val:
                    val = repr(val)
                else:
                    val = '<nil>'
                logMsg += '%s:%s' % (oid.prettyPrint(), val) + ','

        else:
            logMsg = '<nil>'
        return logMsg