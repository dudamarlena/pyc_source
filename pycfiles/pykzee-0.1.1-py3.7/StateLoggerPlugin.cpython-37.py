# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pykzee/StateLoggerPlugin.py
# Compiled at: 2019-10-26 12:11:05
# Size of source mod 2**32: 1610 bytes
import logging
from pyimmutable import ImmutableDict, ImmutableList
import pykzee.Plugin as Plugin

class StateLoggerPlugin(Plugin):

    def init(self, path=(), *, pretty=False):
        self._StateLoggerPlugin__pretty = pretty
        self.unsubscribe = self.subscribe(self.stateUpdate, path)

    def stateUpdate(self, state):
        if not self._StateLoggerPlugin__pretty:
            logging.debug(repr(state))
            return
        logging.debug('StateLoggerPlugin: new state:')
        pretty_print(state, OutputLines(logging.debug))


class OutputLines:

    def __init__(self, write):
        self._OutputLines__write = write
        self._OutputLines__data = ''

    def __call__(self, x):
        self._OutputLines__data += x
        pos = self._OutputLines__data.rfind('\n')
        if pos < 0:
            return
        out = self._OutputLines__data[0:pos]
        self._OutputLines__data = self._OutputLines__data[pos + 1:]
        for line in out.split('\n'):
            self._OutputLines__write(line)

    def __del__(self):
        if self._OutputLines__data:
            self._OutputLines__write(self._OutputLines__data)


def pretty_print(data, write, indent=''):
    if type(data) is ImmutableDict:
        more_indent = indent + '  '
        write('{\n')
        for key, value in data.items():
            write(f"{indent}  {key!r}: ")
            pretty_print(value, write, more_indent)
            write(',\n')

        write(f"{indent}}}")
    else:
        if type(data) is ImmutableList:
            more_indent = indent + '  '
            write('[\n')
            for value in data:
                write(more_indent)
                pretty_print(value, write, more_indent)
                write(',\n')

            write(f"{indent}]")
        else:
            write(repr(data))