# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/UniversalAnalytics/HTTPLog.py
# Compiled at: 2014-12-03 14:59:50
import sys, re, os
from cStringIO import StringIO

class BufferTranslator(object):
    """ Provides a buffer-compatible interface for filtering buffer content.
    """
    parsers = []

    def __init__(self, output):
        self.output = output
        self.encoding = getattr(output, 'encoding', None)
        return

    def write(self, content):
        content = self.translate(content)
        self.output.write(content)

    @staticmethod
    def stripslashes(content):
        return content.decode('string_escape')

    @staticmethod
    def addslashes(content):
        return content.encode('string_escape')

    def translate(self, line):
        for pattern, method in self.parsers:
            match = pattern.match(line)
            if match:
                return method(match)

        return line


class LineBufferTranslator(BufferTranslator):
    """ Line buffer implementation supports translation of line-format input
        even when input is not already line-buffered. Caches input until newlines 
        occur, and then dispatches translated input to output buffer.
    """

    def __init__(self, *a, **kw):
        self._linepending = []
        super(LineBufferTranslator, self).__init__(*a, **kw)

    def write(self, _input):
        lines = _input.splitlines(True)
        for i in range(0, len(lines)):
            last = i
            if lines[i].endswith('\n'):
                prefix = len(self._linepending) and ('').join(self._linepending) or ''
                self.output.write(self.translate(prefix + lines[i]))
                del self._linepending[0:]
                last = -1

        if last >= 0:
            self._linepending.append(lines[last])

    def __del__(self):
        if len(self._linepending):
            self.output.write(self.translate(('').join(self._linepending)))


class HTTPTranslator(LineBufferTranslator):
    """ Translates output from |urllib2| HTTPHandler(debuglevel = 1) into
        HTTP-compatible, readible text structures for human analysis.
    """
    RE_LINE_PARSER = re.compile("^(?:([a-z]+):)\\s*(\\'?)([^\\r\\n]*)\\2(?:[\\r\\n]*)$")
    RE_LINE_BREAK = re.compile('(\\r?\\n|(?:\\\\r)?\\\\n)')
    RE_HTTP_METHOD = re.compile('^(POST|GET|HEAD|DELETE|PUT|TRACE|OPTIONS)')
    RE_PARAMETER_SPACER = re.compile('&([a-z0-9]+)=')

    @classmethod
    def spacer(cls, line):
        return cls.RE_PARAMETER_SPACER.sub(' &\\1= ', line)

    def translate(self, line):
        parsed = self.RE_LINE_PARSER.match(line)
        if parsed:
            value = parsed.group(3)
            stage = parsed.group(1)
            if stage == 'send':
                return '\n# HTTP Request:\n' + self.stripslashes(value)
            if stage == 'reply':
                return '\n\n# HTTP Response:\n' + self.stripslashes(value)
            if stage == 'header':
                return value + '\n'
            return value
        return line


def consume(outbuffer=None):
    sys.stdout = HTTPTranslator(outbuffer or sys.stdout)
    return sys.stdout


if __name__ == '__main__':
    consume(sys.stdout).write(sys.stdin.read())
    print '\n'