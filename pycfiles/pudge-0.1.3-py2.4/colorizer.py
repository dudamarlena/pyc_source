# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.0-Power_Macintosh/egg/pudge/colorizer.py
# Compiled at: 2006-03-14 16:35:23
"""Python source code colorizer.

This module is derived from MoinMoin's [1] python source parser, described
in the following recipe:

<http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52298>

.. [1] http://moin.sourceforge.net/

"""
import cgi, string, sys, cStringIO, keyword, token, tokenize, re
_KEYWORD = token.NT_OFFSET + 1
_TEXT = token.NT_OFFSET + 2
_styles = {token.NUMBER: 'number', token.OP: 'op', token.STRING: 'string', tokenize.COMMENT: 'comment', token.NAME: 'name', token.ERRORTOKEN: 'error', _KEYWORD: 'keyword', _TEXT: 'text'}

class Parser:
    """ Send colored python source."""
    __module__ = __name__

    def __init__(self, filename, out=sys.stdout):
        """ Store the source text.
        """
        self.filename = filename
        self.raw = open(filename, 'r').read().expandtabs().strip()
        self.out = out

    def format(self):
        """ Parse and send the colored source."""
        self.lines = [
         0, 0]
        pos = 0
        while 1:
            pos = self.raw.find('\n', pos) + 1
            if not pos:
                break
            self.lines.append(pos)

        self.lines.append(len(self.raw))
        self.out.write('<html><head><title>%s</title>\n        <script type="text/javascript"><!--\n        %s\n        // --></script>\n        <style>\n        div.python {\n          color: #333\n        }\n        div.python a.lnum {\n          color: #555;\n          background-color: #eee;\n          border-right: 1px solid #999;\n          padding-right: 2px;\n          margin-right: 4px;\n        }\n        div.python span.comment { color: #933 }\n        div.python span.keyword { color: #a3e; font-weight: bold  }\n        div.python span.op { color: #c96 }\n        div.python span.string { color: #6a6 }\n        div.python span.name { }\n        div.python span.text { color: #333 }\n        div.highlighted { background-color: #ff9; border: 1px solid #009 }\n        </style></head><body onload="show_line_range()">' % (cgi.escape(self.filename), highlight_javascript))
        self.out.write('<div class="python"><code>')
        self.write_line(1, br='')
        self.pos = 0
        text = cStringIO.StringIO(self.raw)
        self.run_tokens(tokenize.generate_tokens(text.readline))
        self.out.write('</code></div>')
        self.out.write('</body></html>')
        self.out.flush()
        self.out.close()

    def write_line(self, line_num, br='<br />\n'):
        fmt = str(line_num).rjust(4, '0')
        self.out.write('%s<a class="lnum" href="#%d" name="%d">%s</a>' % (br, line_num, line_num, fmt))

    def run_tokens(self, it):
        """ Token handler."""
        for tok in it:
            (toktype, toktext, (srow, scol), (erow, ecol), line) = tok
            oldpos = self.pos
            newpos = self.lines[srow] + scol
            self.pos = newpos + len(toktext)
            if toktype in [token.NEWLINE, tokenize.NL]:
                self.write_line(srow + 1)
                continue
            if newpos > oldpos:
                ws = self.raw[oldpos:newpos]
                self.out.write('&#0160;' * len(ws))
            if toktype in [token.INDENT, token.DEDENT]:
                self.pos = newpos
                continue
            if token.LPAR <= toktype and toktype <= token.OP:
                toktype = token.OP
            elif toktype == token.NAME and keyword.iskeyword(toktext):
                toktype = _KEYWORD
            style = _styles.get(toktype, _styles[_TEXT])
            self.runlines(toktext, srow, '<span class="%s">%%s</span>' % style)

    def runlines(self, text, line_num, interpolate):
        if '\n' in text:
            lines = text.split('\n')
            for (i, line) in zip(range(len(lines)), lines):
                if i > 0:
                    self.write_line(line_num + i)
                self.out.write(interpolate % cgi.escape(line).replace(' ', '&#0160;'))

        if text:
            self.out.write(interpolate % cgi.escape(text).replace(' ', '&#0160;'))


highlight_javascript = "\nfunction show_line_range() {\n    var href = document.location.href;\n    if (href.indexOf('?') == -1) {\n        return;\n    }\n    var qs = href.substring(href.indexOf('?')+1);\n    if (qs.indexOf('#') >= 0) {\n        qs = qs.substring(0, qs.indexOf('#'));\n    }\n    var first = qs.match(/f=(\\d+)/)[1];\n    var last = qs.match(/l=(\\d+)/)[1];\n    if (! first || ! last) {\n        return;\n    }\n    var anchors = document.getElementsByTagName('A');\n    var container = document.createElement('DIV');\n    container.className = 'highlighted';\n    var children = [];\n    var start = null;\n    var parent = null;\n    var highlight = false;\n    for (var i = 0; i < anchors.length; i++) {\n        var el = anchors[i];\n        if (el.getAttribute('name') == first) {\n            start = el.previousSibling;\n            parent = el.parentNode;\n            highlight = true;\n        }\n        if (el.getAttribute('name') == last) {\n            break;\n        }\n        if (highlight) {\n            children[children.length] = el;\n            el = el.nextSibling;\n            while (el && el.tagName != 'A') {\n                children[children.length] = el;\n                el = el.nextSibling;\n            }\n        }\n    }\n    for (i=0; i<children.length; i++) {\n        container.appendChild(children[i]);\n    }\n    if (start) {\n        start.parentNode.insertBefore(container, start.nextSibling);\n    } else {\n        parent.insertBefore(container, parent.childNodes[0]);\n    }\n}\n"
__all__ = [
 'Parser']
__author__ = 'Ryan Tomayko <rtomayko@gmail.com>'
__date__ = '$Date: 2006-01-08 15:28:12 -0800 (Sun, 08 Jan 2006) $'
__revision__ = '$Revision: 107 $'
__url__ = '$URL: svn://lesscode.org/pudge/trunk/pudge/colorizer.py $'
__copyright__ = 'Copyright 2005, Ryan Tomayko'
__license__ = 'MIT <http://www.opensource.org/licenses/mit-license.php>'