# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ZPTKit/htmlrender.py
# Compiled at: 2006-06-20 16:13:48
"""
A simple renderer for HTML to plain text.  It knows about <p>, <div>,
and <blockquote>; all other markup is ignored.

Paragraphs are collected and wrapped.  Blockquotes are indented.
Paragraphs cannot be nested at this time.  HTML entities are
substituted.  Usually this should only be used with markup that is
intended to be used with this renderer (e.g., ZPTKit.emailtemplate).

The render() function is the easiest way to use this.
"""
from HTMLParser import HTMLParser
try:
    import textwrap
except:
    from backports import textwrap

import re, htmlentitydefs
DEFAULT_ENCODING = 'utf8'

def render(text, width=70):
    context = Context()
    context.width = width
    context.indent = 0
    p = HTMLRenderer()
    p.feed(text)
    p.close()
    paras = [ encode_unicode(para.to_text(context)) for para in p.paragraphs if para ]
    return ('').join(paras)


def encode_unicode(s, encoding=None):
    if isinstance(s, unicode):
        return s.encode(encoding or DEFAULT_ENCODING)
    return s


class HTMLRenderer(HTMLParser):
    __module__ = __name__
    block_tags = ('p div blockquote h1 h2 h3 h4 h5 h6 ul ol').split()

    def reset(self):
        HTMLParser.reset(self)
        self.paragraphs = []
        self.in_paragraph = None
        self.last_href = None
        self.href_content = None
        self.in_table = None
        self.cell_content = None
        self.list_type = []
        return

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == 'body':
            self.paragraphs = []
            self.in_paragraph = None
        if tag == 'blockquote':
            self.paragraphs.append(Indenter(4))
        if tag in self.block_tags:
            self.start_para(tag, attrs)
        if tag == 'br':
            self.add_br(tag, attrs)
        if tag == 'a':
            self.last_href = self.get_attr(attrs, 'href')
            self.href_content = []
        if tag == 'img':
            alt = self.get_attr(attrs, 'alt')
            if alt:
                self.handle_data(alt)
        if tag == 'table':
            if self.in_table:
                self.in_table.depth += 1
            else:
                self.in_table = Table()
        if tag == 'tr':
            self.in_table.add_row()
        if tag == 'td':
            self.cell_content = []
        if tag == 'ul':
            self.paragraphs.append(Indenter(2))
            self.list_type.append('ul')
        if tag == 'ol':
            self.paragraphs.append(Indenter(2))
            self.list_type.append(1)
        if tag == 'li':
            self.add_br(None, None)
            if not self.list_type or self.list_type[(-1)] == 'ul':
                self.handle_data('* ')
            else:
                self.handle_data('%i) ' % self.list_type[(-1)])
                self.list_type[(-1)] += 1
        return

    def handle_endtag(self, tag):
        if tag in self.block_tags:
            self.end_para(tag)
        if tag == 'a':
            if self.href_content:
                content = ('').join(self.href_content)
            else:
                content = None
            self.href_content = None
            if content and self.last_href and content != self.last_href:
                self.handle_data(' <%s>' % self.last_href)
            self.last_href = None
        if tag == 'table':
            self.paragraphs.append(self.in_table)
            self.in_table.depth -= 1
            if not self.in_table.depth:
                self.in_table = None
        if tag == 'td':
            self.end_para(tag)
            if self.paragraphs:
                self.in_table.add_cell(self.paragraphs[(-1)])
                self.paragraphs.pop()
        if tag == 'ul' or tag == 'ol':
            self.paragraphs.append(Indenter(-2))
            self.list_type.pop()
        if tag == 'blockquote':
            self.paragraphs.append(Indenter(-4))
        return

    def handle_data(self, data):
        if self.in_paragraph is None:
            self.start_para(None, None)
        self.in_paragraph.add_text(data)
        if self.href_content is not None:
            self.href_content.append(data)
        return

    def handle_entityref(self, name):
        name = name.lower()
        if name not in htmlentitydefs.entitydefs:
            self.handle_data('&' + name)
            return
        result = htmlentitydefs.entitydefs[name]
        if result.startswith('&'):
            self.handle_charref(result[2:-1])
        else:
            self.handle_data(result)

    def handle_charref(self, name):
        try:
            self.handle_data(unichr(int(name)))
        except ValueError:
            self.handle_data('&' + name)

    def start_para(self, tag, attrs):
        if tag is None:
            tag = 'p'
            attrs = []
        self.end_para(None)
        self.in_paragraph = Paragraph(tag, attrs)
        return

    def end_para(self, tag):
        if self.in_paragraph:
            self.paragraphs.append(self.in_paragraph)
        self.in_paragraph = None
        return

    def add_br(self, tag, attrs):
        if not self.in_paragraph:
            self.start_para(None, None)
        self.in_paragraph.add_tag('<br>')
        return

    def close(self):
        HTMLParser.close(self)
        self.end_para(None)
        return

    def get_attr(self, attrs, name, default=None):
        for (attr_name, value) in attrs:
            if attr_name.lower() == name.lower():
                return value

        return default


class Paragraph:
    __module__ = __name__

    def __init__(self, tag, attrs):
        self.tag = tag
        self.attrs = attrs
        self.text = []
        self._default_align = 'left'

    def __repr__(self):
        length = len(('').join(map(str, self.text)))
        attrs = (' ').join([self.tag] + [ '%s="%s"' % (name, value) for (name, value) in self.attrs ] + ['length=%i' % length])
        return '<Paragraph %s: %s>' % (hex(id(self))[2:], attrs)

    def add_text(self, text):
        self.text.append(text)

    def add_tag(self, tag):
        self.text.append([tag])

    def to_text(self, context):
        lines = self.make_lines()
        width = context.width
        indent = context.indent
        wrapped_lines = []
        for line in lines:
            wrapped = textwrap.wrap(line, width, replace_whitespace=True, initial_indent=' ' * indent, subsequent_indent=' ' * indent, fix_sentence_endings=False, break_long_words=False)
            wrapped_lines.extend(wrapped)

        if self.tag in ('h1', 'h2'):
            self._default_align = 'center'
        lines = self.align_lines(wrapped_lines, width)
        text = ('\n').join(lines)
        if self.tag in ('h1', 'h3'):
            text = text.upper()
        if self.tag == 'h4':
            text = '*%s*' % text
        return text + '\n\n'

    def align_lines(self, lines, width):
        if self.alignment() == 'right':
            return [ ' ' * (width - len(line)) + line for line in lines ]
        elif self.alignment() == 'center':
            return [ ' ' * ((width - len(line)) / 2) + line for line in lines ]
        elif self.alignment() == 'left':
            return lines
        else:
            return lines

    def make_lines(self):
        lines = ['']
        for data in self.text:
            if isinstance(data, list):
                tag = data[0]
                if tag == '<br>':
                    lines.append('')
                else:
                    assert 0, 'Unknown tag: %r' % tag
            else:
                lines[-1] = lines[(-1)] + data

        return [ normalize(line).strip() for line in lines if line ]

    def alignment(self):
        for (name, value) in self.attrs:
            if name.lower() == 'align':
                return value.lower()

        return self._default_align

    def __nonzero__(self):
        for t in self.text:
            if t:
                return True

        return False


class Table:
    __module__ = __name__

    def __init__(self):
        self.rows = []
        self.row_num = 0
        self.depth = 1

    def add_row(self):
        self.row_num += 1
        self.rows.append([])

    def add_cell(self, value):
        self.rows[(-1)].append(value)

    def __nonzero__(self):
        return not not self.rows

    def to_text(self, context):
        if self.rows and not self.rows[(-1)]:
            self.rows.pop()
        if not self.rows:
            return ''
        headers = [ p.to_text(context).strip() for p in self.rows.pop(0) ]
        context.indent += 4
        lines = []
        for row in self.rows:
            for (header, cell) in zip(headers, row):
                cell_text = cell.to_text(context).strip()
                lines.append('%s: %s' % (header, cell_text))

            lines.append('')

        context.indent -= 4
        return ('\n').join(lines) + '\n\n'


class Indenter:
    __module__ = __name__

    def __init__(self, indent):
        self.indent = indent

    def to_text(self, context):
        context.indent += self.indent
        return ''


class Context:
    __module__ = __name__


def normalize(text):
    text = re.sub('\\s+', ' ', text)
    if not isinstance(text, unicode):
        text = text.replace(b'\xa0', ' ')
    return text


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    if not args:
        input = sys.stdin.read()
    else:
        input = open(args[0]).read()
    print render(input)