# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/syntax.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from __future__ import print_function
import re
from .tools import timer, remove_padding
from .compat import iteritems, with_metaclass
from .filter import MoyaFilterBase
from .render import HTML
from .compat import text_type
from textwrap import dedent

def _escape_html(text):
    """Escape text for inclusion in html"""
    return text.replace(b'&', b'&amp;').replace(b'<', b'&lt;').replace(b'>', b'&gt;').replace(b' ', b'&nbsp;')


def tabs_to_spaces(line, tab_size=4):
    """Converts tabs to a fixed numbers of spaces at the beginning of a string"""
    spaces = 0
    for c in line:
        if c not in b' \t':
            break
        if c == b'\t':
            spaces += tab_size - spaces % tab_size
        else:
            spaces += 1

    return b' ' * spaces + line.lstrip()


def highlight(format, code, start_line=1, end_line=None, line_numbers=True, highlight_lines=None, highlight_range=None, highlight_range_style=b'error'):
    if isinstance(code, bytes):
        code = code.decode(b'utf-8', b'replace')
    HL = HighlighterMeta.highlighters.get(format, Highlighter)
    h = HL()
    html = h.highlight(code, start_line, end_line, line_numbers=line_numbers, highlight_lines=highlight_lines, highlight_range=highlight_range, highlight_range_style=highlight_range_style)
    return html


class HighlighterMeta(type):
    highlighters = {}

    def __new__(cls, name, base, attrs):
        new_class = type.__new__(cls, name, base, attrs)
        format = getattr(new_class, b'format', None)
        if format:
            cls.highlighters[format] = new_class
        flags = re.UNICODE | re.MULTILINE | re.DOTALL
        new_class._compiled_styles = [ re.compile(s, flags) for s in new_class.styles ]
        return new_class


class HighlighterType(object):
    """Somewhat naive syntax highlighter"""
    line_anchors = True
    styles = []
    _compiled_styles = None
    _re_linebreaks = re.compile(b'$', flags=re.UNICODE | re.MULTILINE | re.DOTALL)
    _highlight_range_padding = 50

    def highlight(self, code, start_line=None, end_line=None, line_numbers=True, highlight_lines=None, highlight_range=None, highlight_range_style=b'error'):
        if start_line is None:
            start_line = 1
        offset_line = 0
        start_line = max(1, start_line)
        lines = code.splitlines()
        if end_line is None:
            end_line = len(lines)
        lines = [
         b''] * offset_line + lines[offset_line:end_line + self._highlight_range_padding + 1]
        code = (b'\n').join(tabs_to_spaces(l.rstrip()) for l in lines)
        points = []
        line_starts = [
         -1]
        add_point = points.append
        for style_regex in self._compiled_styles:
            for match in style_regex.finditer(code):
                for k, v in iteritems(match.groupdict()):
                    if v:
                        start, end = match.span(k)
                        add_point((start, True, k))
                        add_point((end, False, k))

        def sub_linebreaks(match):
            start = match.start(0)
            line_starts.append(start)
            add_point((start, True, b''))

        self._re_linebreaks.sub(sub_linebreaks, code)
        if highlight_range:
            line_no, start, end = highlight_range
            try:
                line_start = line_starts[(line_no - 1)]
            except IndexError:
                pass
            else:
                hi_start = line_start + start
                hi_end = line_start + end + 1
                add_point((hi_start, True, highlight_range_style))
                add_point((hi_end, False, highlight_range_style))

        points.sort()
        lines_out = []
        hiline = []
        hiline_append = hiline.append
        style_set = set()
        pos = 0
        points = points[::-1]
        while points:
            start_pos, add_style, style = points.pop()
            new_style_set = style_set.copy()
            if style:
                if add_style:
                    new_style_set.add(style)
                else:
                    new_style_set.discard(style)
                while points:
                    peek_start, peek_add, peek_style = points[(-1)]
                    if peek_style and peek_start == start_pos:
                        if peek_add:
                            new_style_set.add(peek_style)
                        else:
                            new_style_set.discard(peek_style)
                        points.pop()
                    else:
                        break

            if start_pos > pos:
                hiline_append(_escape_html(code[pos:start_pos]))
            pos = start_pos
            if not style:
                if style_set:
                    hiline.append(b'</span>')
                lines_out.append(hiline[:])
                del hiline[:]
                if new_style_set:
                    hiline_append(b'<span class="%s">' % (b' ').join(new_style_set))
                style_set = new_style_set
                continue
            if new_style_set != style_set:
                hiline_append(b'</span>')
                if new_style_set:
                    hiline_append(b'<span class="%s">' % (b' ').join(new_style_set))
            style_set = new_style_set

        if hiline:
            lines_out.append(hiline[:])
            lines_out.append(b'</span>')
        if end_line is None:
            lines_out = lines_out[start_line - 1:]
        else:
            lines_out = lines_out[start_line - 1:end_line]

        def make_line(l):
            text = (b'').join(l)
            if text.strip():
                return text.replace(b'\n', b'')
            else:
                return b'\n'

        html_lines = [ make_line(line) for line in lines_out ]
        if line_numbers:
            html_lines = [ (b'<span class="lineno">{0}</span>{1}').format(line_no, line) for line_no, line in enumerate(html_lines, start_line or 0) ]
        if highlight_lines is None:
            highlight_lines = ()
        if self.line_anchors:
            linet = b'<a name="line{1}"></a><div class="line{0} line-{1}">{2}</div>'
        else:
            linet = b'<div class="line{0} line-{1}">{2}</div>'
        html_lines = [ linet.format(b' highlight' if line_no in highlight_lines else b'', line_no, line) for line_no, line in enumerate(html_lines, start_line or 0)
                     ]
        return (b'').join(html_lines).replace(b'\n', b'<br>')


class Highlighter(with_metaclass(HighlighterMeta, HighlighterType)):
    pass


class TextHighlighter(Highlighter):
    format = b'text'


class XMLHighlighter(Highlighter):
    format = b'xml'
    styles = [
     b'(?P<comment><!--.*?-->)|(?P<tag><(?P<xmlns>\\w*?:)?(?P<tagname>[\\w\\-]*)(?P<tagcontent>.*?)(?P<endtagname>/[\\w\\-:]*?)?>)',
     b'\\s\\S*?=(?P<attrib>\\".*?\\")',
     b'(?P<braced>\\{.*?\\})',
     b'(?P<sub>\\$\\{.*?\\})',
     b'(?P<cdata>\\<\\!\\[CDATA\\[.*?\\]\\]\\>)']


class PythonHighlighter(Highlighter):
    format = b'python'
    styles = [
     b'\\b(?P<keyword>yield|is|print|raise|pass|and|or|not|return|def|class|import|from|as|for|in|try|except|with|finally|if|else|elif|while)\\b',
     b'\\b(?P<constant>None|True|False)\\b',
     b'\\b(?P<builtin>open|file|str|repr|bytes|unicode|int)\\b',
     b'\\b\\((?P<call>.*?)\\)',
     b'\\b((?:def|class)\\s+(?P<def>\\w+))',
     b'(?P<self>self)',
     b'\\b(?P<number>\\d+)',
     b'(?P<operator>\\W+)',
     b'\\b(?P<operator>or|and|in)\\b',
     b'(?P<brace>\\(|\\)|\\[|\\]|\\{|\\})',
     b'@(?P<decorator>[\\w\\.]*)',
     b'(?P<comment>#.*?)$|(?P<string>(?:""".*?""")|(?:"(?:\\\\.|.)*?")' + b"|(?:'''.*?''')|(?:'(?:\\\\.|.)*?'))"]


class HTMLHighlighter(Highlighter):
    format = b'html'
    styles = [
     b'(?P<comment><!--.*?-->)|(?P<tag><(?P<xmlns>\\w*?:)?(?P<tagname>\\w*)(?P<tagcontent>.*?)(?P<endtagname>/\\w*?)?>)',
     b'\\s\\S*?=(?P<attrib>\\".*?\\")']


class MoyatemplateHighlighter(Highlighter):
    format = b'moyatemplate'
    styles = [
     b'(?P<comment><!--.*?-->)|(?P<tag><(?P<xmlns>\\w*?:)?(?P<tagname>\\w*)(?P<tagcontent>.*?)(?P<endtagname>/\\w*?)?>)',
     b'\\s\\S*?=(?P<attrib>\\".*?\\")',
     b'(?P<sub>\\$\\{.*?\\})',
     b'(?P<templatetag>{%.*?%})']


class RouteHighlighter(Highlighter):
    format = b'route'
    styles = [
     b'(?P<special>\\{.*?\\})']


class TargetHighlighter(Highlighter):
    line_anchors = False
    format = b'target'
    styles = [
     b'(?P<libname>[\\w\\.\\-]+?)(?P<hash>\\#)(?P<elementname>[\\w\\.\\-]+)']


class INIHighlighter(Highlighter):
    line_anchors = False
    format = b'ini'
    styles = [
     b'^(?P<key>.*?)=(?P<value>.*?)$',
     b'^(\\s+)(?P<value>.*?)$',
     b'^(?P<section>\\[.*?\\])$',
     b'^(?P<section>\\[(?P<sectiontype>.*?)\\:(?P<sectionname>.*?)\\])$',
     b'^(?P<comment>#.*?)$']


class JSHighligher(Highlighter):
    format = b'js'
    styles = [
     b'(?P<keyword>this|function|var|new|alert)',
     b'\\b(?P<constant>null|true|false)\\b',
     b'\\b(?P<number>\\d+)',
     b'(?P<operator>\\W+)',
     b'\\b(?P<operator>\\|\\||\\&\\&|\\+|\\-|\\*|\\/)\\b',
     b'(?P<brace>\\(|\\)|\\[|\\]|\\{|\\})',
     b'(?P<string>".*?")',
     b"(?P<string>\\'.*?\\')",
     b'(?P<comment>\\/\\*.*?\\*\\/)']


class Formatter(object):

    def __init__(self, lineno=True):
        self.lineno = lineno


class HTMLFormatter(Formatter):
    pass


class SyntaxFilter(MoyaFilterBase):

    def __moyafilter__(self, context, app, value, params):
        lang = params.pop(b'lang', None)
        value = dedent(remove_padding(text_type(value.strip(b'\n'))))
        code = highlight(lang, value, line_numbers=False)
        return HTML((b'<pre class="moya-console format-{lang}"">{code}</pre>').format(lang=lang, code=code))


if __name__ == b'__main__':
    code = open(b'console.py', b'rb').read()
    code = code.decode(b'utf-8')
    html = highlight(b'python', code)
    with timer(b'highlight', ms=True):
        html = highlight(b'python', code)
    with open(b'syntaxtest.html', b'wt') as (f):
        f.write(html.encode(b'utf-8'))