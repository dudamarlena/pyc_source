# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpsim/record/dump.py
# Compiled at: 2018-12-30 10:46:50
import sys
from pyasn1.type import univ
from pyasn1.error import PyAsn1Error
from snmpsim.grammar import dump
from snmpsim.error import SnmpsimError
from snmpsim.record import abstract

class DumpRecord(abstract.AbstractRecord):
    __module__ = __name__
    grammar = dump.DumpGrammar()
    ext = 'dump'

    def evaluateOid(self, oid):
        return univ.ObjectIdentifier(oid)

    def evaluateValue(self, oid, tag, value, **context):
        try:
            value = self.grammar.tagMap[tag](value)
        except:
            raise SnmpsimError('value evaluation error for tag %r, value %r' % (tag, value))

        try:
            if not context['nextFlag'] and not context['exactMatch'] or context['setFlag']:
                return (
                 context['origOid'], tag, context['errorStatus'])
        except KeyError:
            pass

        return (
         oid, tag, value)

    def evaluate(self, line, **context):
        (oid, tag, value) = self.grammar.parse(line)
        oid = self.evaluateOid(oid)
        if context.get('oidOnly'):
            value = None
        else:
            try:
                (oid, tag, value) = self.evaluateValue(oid, tag, value, **context)
            except PyAsn1Error:
                raise SnmpsimError('value evaluation for %s = %r failed: %s\r\n' % (oid, value, sys.exc_info()[1]))

        return (
         oid, value)

    def formatOid(self, oid):
        return univ.ObjectIdentifier(oid).prettyPrint()

    def formatValue(self, oid, value, **context):
        return (
         self.formatOid(oid), self.grammar.getTagByType(value), str(value))

    def format(self, oid, value, **context):
        (textOid, textTag, textValue) = self.formatValue(oid, value, **context)
        return self.grammar.build(textOid, textTag, textValue)