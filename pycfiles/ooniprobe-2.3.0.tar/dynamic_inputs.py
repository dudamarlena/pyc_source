# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x/code/OONI/ooni-probe/ooni/nettests/experimental/dynamic_inputs.py
# Compiled at: 2016-05-20 13:44:30
from ooni.utils import log
from ooni import nettest

class DynamicInputTest(nettest.NetTestCase):
    inputFile = [
     'file', 'f', None,
     'List of things to test']
    requiredOptions = ['file']

    def inputProcessor(self, filename):
        with open(filename) as (f):
            for line in f:
                log.msg('Yielding a line %s' % line.strip())
                result = yield line.strip()
                log.msg('Result of yield %s' % result)
                yield line.strip()

    def test_something(self):
        self.inputs.send('Something %s' % self.input)


class DynamicInputTestTwo(nettest.NetTestCase):
    inputFile = [
     'file', 'f', None,
     'List of things to test']
    requiredOptions = ['file']

    def inputProcessor(self, filename):
        with open(filename) as (f):
            for line in f:
                log.msg('Yielding a line %s' % line.strip())
                result = yield 'two-%s' % line.strip()
                log.msg('Result of yield %s' % result)
                yield 'two-%s' % line.strip()

    def test_something(self):
        self.inputs.send('Something %s' % self.input)