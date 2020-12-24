# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/plist/plistwriter.py
# Compiled at: 2012-10-12 07:02:39
from StringIO import StringIO

class PListWriter:

    def __init__(self):
        self.buf = StringIO()

    def store(self, payload):
        self.buf.write('{\n')
        self.indent = 0
        if isinstance(payload, dict):
            for key in payload.keys():
                self._append(key, payload[key])

        self.buf.write('}')
        return self.buf.getvalue()

    def _requires_quoting(self, value):
        if isinstance(value, basestring):
            if value.isalnum():
                return False
            return True
        raise 'Only string values can be quoted.'

    def _append(self, key, value):
        self._inc_indent()
        self._append_key(key)
        if isinstance(value, basestring):
            self._append_string(value)
        elif isinstance(value, int):
            self._append_integer(value)
        elif isinstance(value, list):
            self._append_array(value)
        elif isinstance(value, dict):
            self._append_dictionary(value)
        else:
            raise 'Unsupported type in plist'
        self._append_suffix()
        self._dec_indent()

    def _inc_indent(self):
        self.indent = self.indent + 1

    def _dec_indent(self):
        self.indent = self.indent - 1

    def _append_indent(self):
        count = 0
        while count < self.indent:
            self.buf.write('    ')
            count = count + 1

    def _append_suffix(self):
        self.buf.write(';\n')

    def _append_key(self, key):
        self._append_indent()
        if self._requires_quoting(key):
            self.buf.write('"%s" = ' % key)
        else:
            self.buf.write('%s = ' % key)

    def _append_string(self, value):
        if self._requires_quoting(value):
            self.buf.write('"%s"' % value.replace('"', '\\"'))
        else:
            self.buf.write(value)

    def _append_integer(self, value):
        self.buf.write('%d' % value)

    def _append_array(self, value):
        self.buf.write('(\n')
        self._inc_indent()
        i = 0
        while i < len(value):
            self._append_indent()
            x = value[i]
            if isinstance(x, basestring):
                self._append_string(x)
            elif isinstance(x, int):
                self._append_integer(x)
            elif isinstance(x, list):
                self._append_array(x)
            elif isinstance(x, dict):
                self._append_dictionary(x)
            i = i + 1
            if i < len(value):
                self.buf.write(',\n')
            else:
                self.buf.write('\n')

        self._dec_indent()
        self._append_indent()
        self.buf.write(')')

    def _append_dictionary(self, value):
        self.buf.write('{\n')
        i = 0
        while i < len(value.keys()):
            k = value.keys()[i]
            v = value[k]
            self._append(k, v)
            i = i + 1

        self._append_indent()
        self.buf.write('}')