# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/nosespec.py
# Compiled at: 2010-11-05 06:26:31
import logging, inspect, re
from nose.plugins import Plugin
NAMES_RE = re.compile('[Tt]est')
RED = '\x1b[22;31m'
GREEN = '\x1b[22;32m'
WHITE = '\x1b[01;37m'

class Message(object):

    def __init__(self, text, color):
        self.text = '%s%s%s' % (color, text, WHITE)

    def __str__(self):
        return self.text


class SpecPlugin(Plugin):
    messages = {}

    def addSuccess(self, test):
        self.messages[self.spec_name].append(Message(test.address()[(-1)].split('.')[(-1)], GREEN))

    def addFailure(self, test, err):
        self.messages[self.spec_name].append(Message(test.address()[(-1)].split('.')[(-1)], RED))

    def addError(self, test, err):
        self.messages[self.spec_name].append(Message(test.address()[(-1)].split('.')[(-1)], RED))

    def startContext(self, context):
        if inspect.ismodule(context):
            self.spec_name = False
            return
        self.spec_name = str(context).split('.')[(-1)]
        self.messages[self.spec_name] = list()

    def setOutputStream(self, stream):
        self.stream = stream
        return stream

    def finalize(self, result):
        self.stream.writeln('-------')
        for (key, value) in self.messages.iteritems():
            self.writeln(key)
            for x in value:
                self.writeln(' -%s' % x)

    def writeln(self, value):
        self.stream.writeln(self._clean(value))

    def _clean(self, value):
        return NAMES_RE.sub('', value).replace('_', ' ')