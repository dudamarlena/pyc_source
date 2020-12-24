# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/shakespeare/tests/test_format.py
# Compiled at: 2008-10-29 17:02:16
import StringIO, shakespeare.format
starttext = unicode('Blah æ\nblah & blah', 'utf-8')
sometext = starttext.replace('&', '&amp;')

class TestTextFormatter:
    formatter = shakespeare.format.TextFormatter()

    def test_escape_chars(self):
        out = self.formatter.escape_chars(starttext)
        assert out == sometext


class TestTextFormatterPlain:
    fileobj = StringIO.StringIO(starttext.encode('utf-8'))
    formatter = shakespeare.format.TextFormatterPlain()
    exp = '\n<pre>\n    %s\n</pre>' % sometext

    def test_format(self):
        out = self.formatter.format(self.fileobj)
        assert out == self.exp


class TestTextFormatterLineno:
    fileobj = StringIO.StringIO(starttext.encode('utf-8'))
    formatter = shakespeare.format.TextFormatterLineno()
    exp = '<pre id="0">0    Blah æ</pre>\n<pre id="1">1    blah &amp; blah</pre>\n'

    def test_format(self):
        out = self.formatter.format(self.fileobj)
        assert out == self.exp


def test_text_format():
    formatlist = [
     (
      'plain', TestTextFormatterPlain),
     (
      'lineno', TestTextFormatterLineno)]
    for item in formatlist:
        fileobj = StringIO.StringIO(starttext.encode('utf-8'))
        tout = shakespeare.format.format_text(fileobj, item[0])
        assert tout == item[1].exp