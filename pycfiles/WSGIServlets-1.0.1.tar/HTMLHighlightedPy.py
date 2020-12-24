# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/HTMLHighlightedPy.py
# Compiled at: 2011-05-21 09:59:18
import tokenize, keyword, cgi
from cStringIO import StringIO

class HTMLHighlightedPy:
    colors = {'NUMBER': 'blue', 'STRING': 'brown', 
       'COMMENT': 'red', 
       'DEF': 'green', 
       'KEYWORD': 'blue'}
    bgcolor = '#dddddd'

    def __init__(self, src):
        lines = [
         None, 0]
        pos = 0
        while True:
            pos = src.find('\n', pos) + 1
            if not pos:
                break
            lines.append(pos)

        pos = 0
        prev_tok_is_def = False
        out = StringIO()
        for (tok_type, tok_str, (srow, scol), (erow, ecol), line) in tokenize.generate_tokens(StringIO(src).readline):
            newpos = lines[srow] + scol
            iskeyword = tok_type == tokenize.NAME and keyword.iskeyword(tok_str)
            isdefname = tok_type == tokenize.NAME and prev_tok_is_def
            if newpos > pos:
                out.write(cgi.escape(src[pos:newpos]))
                pos = newpos
            if iskeyword:
                color = self.colors.get('KEYWORD')
            elif isdefname:
                color = self.colors.get('DEF')
            else:
                color = self.colors.get(tokenize.tok_name[tok_type])
            escaped = cgi.escape(tok_str)
            if color:
                out.write('<span style="color:%s">%s</span>' % (color, escaped))
            else:
                out.write(escaped)
            pos += len(tok_str)
            prev_tok_is_def = iskeyword and tok_str in ('def', 'class')

        self.html = '\n<pre id="src" style="display:none;background-color:%s;padding:10px;border-style:solid">\n%s\n</pre>\n' % (self.bgcolor, out.getvalue())
        out.close()
        return

    def __str__(self):
        return self.html


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print >> sys.stderr, 'usage: %s python_file' % sys.argv[0]
        sys.exit(1)
    try:
        src = open(sys.argv[1]).read()
    except IOError, msg:
        print >> sys.stderr, msg
        sys.exit(1)
    else:
        print '<html>\n<head>\n<title>%s</title>\n</head>\n<body>'
        print HTMLHighlightedPy(src)
        print '</body>\n</html>'