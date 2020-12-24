# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpsim/record/abstract.py
# Compiled at: 2018-12-30 10:46:50
from snmpsim.grammar import abstract
from snmpsim.error import SnmpsimError

class AbstractRecord:
    __module__ = __name__
    grammar = abstract.AbstractGrammar()
    ext = ''

    def evaluateOid(self, oid):
        raise SnmpsimError('Method not implemented at %s' % self.__class__.__name__)

    def evaluateValue(self, oid, tag, value, **context):
        raise SnmpsimError('Method not implemented at %s' % self.__class__.__name__)

    def evaluate(self, line, **context):
        raise SnmpsimError('Method not implemented at %s' % self.__class__.__name__)

    def formatOid(self, oid):
        raise SnmpsimError('Method not implemented at %s' % self.__class__.__name__)

    def formatValue(self, oid, value, **context):
        raise SnmpsimError('Method not implemented at %s' % self.__class__.__name__)

    def format(self, oid, value, **context):
        raise SnmpsimError('Method not implemented at %s' % self.__class__.__name__)