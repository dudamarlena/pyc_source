# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alteraparser/io/output.py
# Compiled at: 2015-12-30 04:57:43
# Size of source mod 2**32: 1060 bytes
import os

class Output(object):

    def write(self, text):
        pass

    def writeln(self, text=''):
        self.write(text + os.linesep)


class ConsoleOutput(Output):

    def write(self, text):
        print(text, end='')


class BufferedOutput(Output):

    def __init__(self):
        self._BufferedOutput__line = ''
        self._BufferedOutput__lines = []

    def write(self, text):
        self._BufferedOutput__line += text

    def writeln(self, text=''):
        self._BufferedOutput__line += text
        self._BufferedOutput__lines.append(self._BufferedOutput__line)
        self._BufferedOutput__line = ''

    def get_lines(self):
        if self._BufferedOutput__line:
            return self._BufferedOutput__lines + [self._BufferedOutput__line]
        else:
            return self._BufferedOutput__lines


class FileOutput(Output):

    def __init__(self, file_path):
        self._FileOutput__file_path = file_path
        self._FileOutput__file = None

    def open(self):
        if self._FileOutput__file:
            self._FileOutput__file.close()
        self._FileOutput__file = open(self._FileOutput__file_path, 'w')

    def close(self):
        self._FileOutput__file.close()
        self._FileOutput__file = None

    def write(self, text):
        self._FileOutput__file.write(text)