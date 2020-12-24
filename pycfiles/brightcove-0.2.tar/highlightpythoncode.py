# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/brightcontent/highlightpythoncode.py
# Compiled at: 2006-06-04 22:32:43
import py2html, os, tempfile

class HighlighterExtension:
    __module__ = __name__
    style = py2html.py_style
    for (key, value) in style.iteritems():
        value[0] += ' '

    def __init__(self):
        self.CODE_RE = '\\[\\[\\[(.*?)\\]\\]\\]'

    def extendMarkdown(self, md):
        self.md = md
        escape_idx = md.inlinePatterns.index(ESCAPE_PATTERN) + 1
        md.inlinePatterns.insert(escape_idx, HighlighterPattern(self.CODE_RE, self))


class HighlighterPattern(BasePattern):
    __module__ = __name__

    def __init__(self, pattern, ext):
        BasePattern.__init__(self, pattern)
        self.ext = ext

    def handleMatch(self, m, doc):
        code = m.group(2).strip()
        (fd, fname) = tempfile.mkstemp()
        f = file(fname, 'w')
        f.write(code)
        f.close()
        result = py2html.file2HTML(fname, 0, self.ext.style, True)
        os.unlink(fname)
        place_holder = self.ext.md.htmlStash.store(result)
        return doc.createTextNode(place_holder)