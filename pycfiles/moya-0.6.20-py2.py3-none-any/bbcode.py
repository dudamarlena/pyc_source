# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/bbcode.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from .compat import implements_to_string
from .html import slugify
from .tools import remove_padding
from .filter import MoyaFilterParams
from . import namespaces
from collections import namedtuple
from fs.path import relativefrom, dirname
import re, textwrap

class BBCodeError(Exception):
    pass


class MultiReplace(object):

    def __init__(self, repl_dict):
        keys = sorted(repl_dict.keys(), reverse=True)
        pattern = (b'|').join([ re.escape(key) for key in keys ])
        self.pattern = re.compile(pattern)
        self.dict = repl_dict
        self.sub = self.pattern.sub

    def replace(self, s):
        get = self.dict.get

        def repl(match):
            item = match.group(0)
            return get(item, item)

        return self.sub(repl, s)

    __call__ = replace


html_escape = MultiReplace({b'<': b'&lt;', b'>': b'&gt;', 
   b'&': b'&amp;', 
   b'\n': b'<br/>'})

@implements_to_string
class Tag(object):
    inline = True
    enclosed = False
    auto_close = False
    visible = True
    html_open = b''
    html_close = b''

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return (b'[{}]').format(self.name)

    def match(self, tag_name):
        return tag_name.lower() == self.name

    def on_insert(self, attribs, data):
        self.attribs = attribs

    def render_open(self, data):
        return self.html_open

    def render_close(self, data, text=None):
        return self.html_close


class BlockTag(Tag):
    inline = False


class FieldTag(Tag):
    auto_close = True

    def on_insert(self, attribs, data):
        data[self.name] = attribs


class ParagraphTag(Tag):
    inline = False
    html_open = b'<p>'
    html_close = b'</p>\n'


class SimpleBlockTag(BlockTag):

    def __init__(self, name, cls):
        super(SimpleBlockTag, self).__init__(name)
        self.html_open = (b'<div class="{}">').format(cls)
        self.html_close = b'</div>'


class InlineTag(Tag):
    inline = True
    enclosed = False
    auto_close = False
    visible = True

    def __init__(self, name, html_open, html_close):
        super(InlineTag, self).__init__(name)
        self.html_open = html_open
        self.html_close = html_close

    def render_open(self, data):
        return self.html_open

    def render_close(self, data, text=None):
        return self.html_close


class InlineCodeTag(Tag):
    inline = True
    enclosed = True
    auto_close = False
    visible = True

    def render_close(self, data, text=None):
        return (b'<code>{}</code>').format(html_escape(text))


class SettingTag(InlineCodeTag):

    def render_close(self, data, text=None):
        if b'=' in text:
            k, v = text.split(b'=', 1)
            k = html_escape(k)
            v = (b'<span class="value">{}</span>').format(html_escape(v))
            return (b'<p class="setting">{}={}</p>').format(k, v)
        return (b'<p class="setting">{}</p>').format(html_escape(text))


class RawTag(Tag):
    inline = True
    visible = True
    enclosed = True

    def render_close(self, data, text=None):
        return text or b''


class AlertTag(BlockTag):
    html_close = b'</div>'

    def render_open(self, data):
        html = b'<div class="alert alert-warning">'
        if self.attribs.strip():
            html += (b'<strong>{}</strong> ').format(self.attribs)
        return html


class AsideTag(BlockTag):
    html_close = b'</aside>'

    def render_open(self, data):
        html = b'<aside>'
        if self.attribs.strip():
            html += (b'<strong>{}</strong> ').format(self.attribs)
        return html


class NoteTag(BlockTag):
    html_open = b'<p class="note">'
    html_close = b'</p>'


class CodeTag(BlockTag):
    enclosed = True
    inline = True

    def render_open(self, data):
        self.lang = self.attribs.strip().lower()
        return (b'<pre class="moya-console format-{}">').format(self.lang)

    def render_close(self, data, text=None):
        from .syntax import highlight
        html = highlight(self.lang, remove_padding(text), line_numbers=False)
        return html + b'</pre>'


class H1Tag(BlockTag):
    inline = False
    enclosed = True
    level = 1

    def render_close(self, data, text=None):
        title = text.strip()
        data.setdefault(b'docmap', []).append([self.level, title])
        h_format = b'<h{level}><a name="{anchor}"></a><a href="#{anchor}">{text}<span class="anchor"> &#182;</span></a></h{level}>'
        return h_format.format(text=html_escape(text), level=self.level + 1, anchor=slugify(title))


class H2Tag(H1Tag):
    level = 2


class H3Tag(H1Tag):
    level = 3


class H4Tag(H1Tag):
    level = 4


Index = namedtuple(b'Index', [b'type', b'template', b'lines'])

class IndexTag(BlockTag):
    enclosed = True

    def render_close(self, data, text=None):
        text = text or b''
        index_name = self.attribs.strip() or b'main'
        index_type = b'1'
        template = None
        if b' ' in index_name:
            index_name, index_type = index_name.split(b' ', 1)
            if b' ' in index_type:
                index_type, template = index_type.split(b' ', 1)
        lines = [ line.strip() for line in text.splitlines() if line.strip() ]
        data.setdefault(b'indices', {})[index_name] = Index(index_type, template, lines)
        return b'{{{' + (b'INDEX {}').format(index_name) + b'}}}'


class URLTag(Tag):
    inline = True

    def render_open(self, data):
        url = self.attribs.strip()
        return (b'<a href="{}">').format(url)

    def render_close(self, data, text=None):
        return b'</a>'


class DocTag(Tag):
    inline = True
    auto_close = True
    _format = b'<a href="{url}">{title}</a>'

    def render_open(self, data):
        pass

    def render_close(self, data, text=None):
        doc_name = self.attribs.strip()
        fragment = None
        if b'#' in doc_name:
            doc_name, fragment = doc_name.split(b'#', 1)
        if b'docs' not in data:
            return doc_name
        else:
            doc = data[b'docs'].get((b'doc.{}').format(doc_name))
            if not doc:
                return doc_name
            title = doc.data.get(b'title', doc_name)
            urls = data[b'urls']
            url = urls[b'doc'].get(doc_name, b'')
            if fragment is not None:
                url = url + b'#' + fragment
            context = data[b'context']
            path = dirname(context.get(b'.request.path', b'/'))
            return self._format.format(title=title, url=relativefrom(path, url))


class DocLinkTag(Tag):
    inline = True
    auto_close = False

    def render_open(self, data):
        doc_name = self.attribs.strip()
        anchor = None
        if b'#' in doc_name:
            doc_name, anchor = doc_name.split(b'#', 1)
        if b'docs' not in data:
            return doc_name
        else:
            doc = data[b'docs'].get((b'doc.{}').format(doc_name))
            if not doc:
                return doc_name
            title = doc.data.get(b'title', doc_name)
            urls = data[b'urls']
            url = urls[b'doc'].get(doc_name, b'')
            context = data[b'context']
            path = dirname(context.get(b'.request.path', b'/'))
            if anchor:
                url = (b'{}#{}').format(url, anchor)
            return (b'<a href="{url}" title="{title}">').format(url=relativefrom(path, url), title=title)

    def render_close(self, data, text=None):
        return b'</a>'


class TagTag(BlockTag):
    inline = True
    auto_close = False
    enclosed = True
    _re_namespace = re.compile(b'^\\{(.*?)\\}(.*?)$')

    @classmethod
    def _join(cls, ns, name):
        if name:
            return (b'{}/{}').format(ns, name)
        return ns

    def render_open(self, data):
        return b''

    def render_close(self, data, text=None):
        if b'context' not in data:
            return (b'<code>{}</code>').format(text)
        else:
            context = data[b'context']
            path = dirname(context.get(b'.request.path', b'/'))
            urls = context[b'.urls']
            tag_name = text.strip()
            xmlns = None
            if b'{' in tag_name:
                xmlns, tag_name = self._re_namespace.match(tag_name).groups()
                if b'://' not in xmlns:
                    xmlns = self._join(namespaces.default, xmlns)
                text = tag_name
                tag_name = (b'{{{}}}{}').format(xmlns, tag_name)
            if xmlns is None:
                xmlns = self.attribs.strip()
                if b'://' not in xmlns:
                    xmlns = self._join(namespaces.default, xmlns)
                tag_name = (b'{{{}}}{}').format(xmlns, tag_name)
            try:
                tag_path = urls[b'tag'][tag_name]
                relative_tag_path = relativefrom(path, tag_path)
            except KeyError as e:
                return (b'<code>{}</code>').format(text)

            return (b'<a class="tag" href="{tag_path}">&lt;{text}&gt;</a>').format(tag_path=relative_tag_path, text=text)
            return


class DefinitionsTag(BlockTag):

    def render_open(self, data):
        return b'<dl class="dl-horizontal">'

    def render_close(self, data, text=None):
        return b'</dl>'


class DefineTag(BlockTag):
    inline = True

    def render_open(self, data):
        return (b'<dt>{}</dt>\n<dd>').format(html_escape(self.attribs))

    def render_close(self, data, text=None):
        return b'</dd>'


class BreakTag(BlockTag):
    inline = True
    auto_close = True

    def render_close(self, data, text=None):
        return b'<br>'


_re_remove_markup = re.compile(b'\\[.*?\\]', re.DOTALL | re.UNICODE)
_re_break_groups = re.compile(b'[\n]{2,}', re.DOTALL | re.UNICODE)

class BBCode(object):
    standard_replace = MultiReplace({b'<': b'&lt;', b'>': b'&gt;', 
       b'&': b'&amp;', 
       b'\n': b'<br/>'})
    standard_unreplace = MultiReplace({b'&lt;': b'<', b'&gt;': b'>', 
       b'&amp;': b'&'})
    standard_replace_no_break = MultiReplace({b'<': b'&lt;', b'>': b'&gt;', 
       b'&': b'&amp;'})
    cosmetic_replace = MultiReplace({b'--': b'&ndash;', b'---': b'&mdash;', 
       b'...': b'&#8230;', 
       b'(c)': b'&copy;', 
       b'(reg)': b'&reg;', 
       b'(tm)': b'&trade;'})
    _re_tag_on_line = re.compile(b'\\[.*?\\]', re.UNICODE)
    _re_end_eq = re.compile(b'\\]|\\=', re.UNICODE)
    _re_quote_end = re.compile(b'\\"|\\]', re.UNICODE)
    _re_tag_token = re.compile(b'^\\[(\\S*?)[\\s=]\\"?(.*?)\\"?\\]$', re.UNICODE)
    _re_new_paragraph = re.compile(b'\\n*?', re.UNICODE)

    def __init__(self):
        self.registry = []
        self.data = {}
        self.add_tag(ParagraphTag, b'p')

    def add_tag(self, tag_class, *args, **kwargs):
        tag_instance = tag_class(*args, **kwargs)
        self.registry.append(tag_instance)

    @classmethod
    def get_locations(cls, post):
        pos_to_location = {}
        line_start = 0
        for line_no, line in enumerate(post.splitlines(True)):
            line_length = len(line)
            for row in range(line_length):
                pos_to_location[line_start + row] = (
                 line_no, row)

            line_start += line_length

        return pos_to_location

    @classmethod
    def tokenize(cls, post):
        locations = cls.get_locations(post)
        re_tag_on_line = cls._re_tag_on_line
        re_end_eq = cls._re_end_eq
        re_quote_end = cls._re_quote_end
        pos = 0

        def find_first(post, pos, re_ff):
            search = re_ff.search(post, pos)
            if search is None:
                return -1
            else:
                return search.start()

        TOKEN_TAG, TOKEN_PTAG, TOKEN_TEXT, TOKEN_PARAGRAPH = range(4)

        def yield_text(text):
            while b'\n\n' in text:
                old_paragraph, text = text.split(b'\n\n', 1)
                if old_paragraph:
                    yield (
                     TOKEN_TEXT, old_paragraph)
                yield (
                 TOKEN_PARAGRAPH, b'\n\n')

            if text:
                yield (
                 TOKEN_TEXT, text)

        post_find = post.find
        while True:
            brace_pos = find_first(post, pos, re_tag_on_line)
            if brace_pos == -1:
                if pos < len(post):
                    for tag_type, text in yield_text(post[pos:]):
                        yield (
                         locations[pos], tag_type, text)

                return
            if brace_pos - pos > 0:
                for tag_type, text in yield_text(post[pos:brace_pos]):
                    yield (
                     locations[pos], tag_type, text)

            pos = brace_pos
            end_pos = pos + 1
            open_tag_pos = post_find(b'[', end_pos)
            end_pos = find_first(post, end_pos, re_end_eq)
            if end_pos == -1:
                for tag_type, text in yield_text(post[pos:]):
                    yield (
                     locations[pos], tag_type, text)

                return
            if open_tag_pos != -1 and open_tag_pos < end_pos:
                for tag_type, text in yield_text(post[pos:open_tag_pos]):
                    yield (
                     locations[pos], tag_type, text)

                end_pos = open_tag_pos
                pos = end_pos
                continue
            if post[end_pos] == b']':
                yield (
                 locations[pos], TOKEN_TAG, post[pos:end_pos + 1])
                pos = end_pos + 1
                continue
            if post[end_pos] == b'=':
                try:
                    end_pos += 1
                    while post[end_pos] == b' ':
                        end_pos += 1

                    if post[end_pos] != b'"':
                        end_pos = post_find(b']', end_pos + 1)
                        if end_pos == -1:
                            return
                        for tag_type, text in yield_text(post[pos:end_pos + 1]):
                            yield (
                             locations[pos], tag_type, text)

                    else:
                        end_pos = find_first(post, end_pos, re_quote_end)
                        if end_pos == -1:
                            return
                        if post[end_pos] == b'"':
                            end_pos = post_find(b'"', end_pos + 1)
                            if end_pos == -1:
                                return
                            end_pos = post_find(b']', end_pos + 1)
                            if end_pos == -1:
                                return
                            yield (
                             locations[pos], TOKEN_PTAG, post[pos:end_pos + 1])
                        else:
                            yield (
                             locations[pos], TOKEN_TAG, post[pos:end_pos + 1])
                    pos = end_pos + 1
                except IndexError:
                    return

    @classmethod
    def parse_tag_token(cls, s):
        m = cls._re_tag_token.match(s.lstrip())
        if m is None:
            name, attribs = s[1:-1], b''
        else:
            name, attribs = m.groups()
        if name.startswith(b'/'):
            return (name.strip()[1:].lower(), attribs.strip(), True)
        else:
            return (
             name.strip().lower(), attribs.strip(), False)
            return

    _re_blank_tags = re.compile(b'\\<(\\w+?)\\>\\</\\1\\>')
    _re_blank_with_spaces_tags = re.compile(b'\\<(\\w+?)\\>\\s+\\</\\1\\>')
    _re_whitespace_word = re.compile(b'(\\s+?\\S*)')

    @classmethod
    def cleanup_html(cls, html):
        """Cleans up html. Currently only removes blank tags, i.e. tags containing only
        whitespace. Only applies to tags without attributes. Tag removal is done
        recursively until there are no more blank tags. So <strong><em></em></strong>
        would be completely removed.

        html -- A string containing (X)HTML

        """
        original_html = b''
        while original_html != html:
            original_html = html
            html = cls._re_blank_tags.sub(b' ', html)
            html = cls._re_blank_with_spaces_tags.sub(b' ', html)

        return html

    def wrap(self, bbcode, max_length=79):
        TOKEN_TAG, TOKEN_PTAG, TOKEN_TEXT, TOKEN_PARAGRAPH = range(4)
        lines = []
        line_length = 0
        bbcode = textwrap.dedent(bbcode.strip(b'\n'))
        for l in bbcode.splitlines():
            lines.append([])
            line_length = 0
            for loc, tag_type, tag_token in self.tokenize(l):
                if not tag_token:
                    continue
                if tag_type == TOKEN_TEXT:
                    for word in self._re_whitespace_word.split(tag_token):
                        if not word:
                            continue
                        if line_length + len(word) > max_length:
                            word = word.lstrip()
                            lines.append([word])
                            line_length = len(word)
                        else:
                            lines[(-1)].append(word)
                            line_length += len(word)

                else:
                    lines[(-1)].append(tag_token)

        return (b'\n\n').join((b'').join(word for word in line) for line in lines)

    def render_console(self, bbcode, max_length=79):
        from .console import AttrText, style, XMLHighlighter
        bbcode = self.wrap(bbcode, max_length=min(120, max_length)) + b'\n'
        TOKEN_TAG, TOKEN_PTAG, TOKEN_TEXT, TOKEN_PARAGRAPH = range(4)
        _bbcode_map = {b'b': b'bold', 
           b'i': b'italic', 
           b'c': b'bold cyan', 
           b'u': b'underline', 
           b'd': b'dim', 
           b'tag': b'bold cyan', 
           b'code': b'bold', 
           b'note': b'italic', 
           b'error': b'bold red', 
           b'success': b'bold green'}
        tag_stack = []
        text = []
        pos = 0
        attributes = []
        for loc, tag_type, tag_token in self.tokenize(bbcode):
            if tag_type == TOKEN_TEXT:
                text += tag_token
                pos += len(tag_token)
            elif tag_type in (TOKEN_TAG, TOKEN_PTAG):
                tag_name, tag_attribs, end_tag = self.parse_tag_token(tag_token)
                if end_tag:
                    try:
                        if tag_name == tag_stack[(-1)][0]:
                            tag_name, attribute_start, tag_style = tag_stack.pop()
                            attributes.append((attribute_start, pos, tag_style))
                    except IndexError:
                        raise ValueError((b"end tag {} doesn't match an opening tag").format(tag_token))

                elif tag_name in _bbcode_map:
                    tag_style = style(_bbcode_map[tag_name])
                    tag_stack.append((tag_name, pos, tag_style))
                else:
                    tag_stack.append((tag_name, pos, None))
                    if not self.supports_tag(tag_name):
                        text += tag_token
                        pos += len(tag_token)
            elif tag_type == TOKEN_PARAGRAPH:
                text.append(b'\n')
                pos += 1

        text = AttrText((b'').join(text))
        text = XMLHighlighter.highlight(text)
        for start, end, tag_style in attributes:
            if tag_style is not None:
                text.add_span(start=start, end=end, **tag_style)

        return text

    def render(self, text, data=None, path=b'?'):
        TOKEN_TAG, TOKEN_PTAG, TOKEN_TEXT, TOKEN_PARAGRAPH = range(4)
        if data is None:
            data = {}

        def raise_error(text):
            raise BBCodeError((b'File "{}", line {}, col {}: {}').format(path, line + 1, col + 1, text))

        html = []
        add_html = html.append
        tag_stack = []
        enclosed_text = []
        add_enclosed_text = enclosed_text.append

        def html_escape(s):
            return s.replace(b'&', b'&amp;').replace(b'<', b'&lt;').replace(b'>', b'&gt;')

        for (line, col), tag_type, tag_token in self.tokenize(text):
            if tag_stack and tag_stack[(-1)].enclosed:
                if tag_type in (TOKEN_TAG, TOKEN_PTAG):
                    tag_name, tag_attribs, end_tag = self.parse_tag_token(tag_token)
                    if end_tag and tag_name.lower() == tag_stack[(-1)].name:
                        try:
                            tag = tag_stack.pop()
                        except IndexError:
                            raise_error((b'Unexpected close tag: {}').format(tag_token))

                        text = (b'').join(enclosed_text)
                        add_html(tag.render_close(data, text=text) or b'')
                        del enclosed_text[:]
                    else:
                        add_enclosed_text(tag_token)
                else:
                    add_enclosed_text(tag_token)
                continue
            if tag_type == TOKEN_TEXT:
                if not tag_stack:
                    ptag = self.get_tag(b'p', b'', data)
                    tag_stack.append(ptag)
                    add_html(ptag.render_open(data) or b'')
                if not enclosed_text:
                    add_html(self.cosmetic_replace(html_escape(tag_token)))
                else:
                    add_html(html_escape(tag_token))
            elif tag_type == TOKEN_PARAGRAPH:
                if tag_stack and tag_stack[(-1)].name == b'p':
                    tag = tag_stack.pop()
                    add_html(tag.render_close(data) or b'')
            elif tag_type in (TOKEN_TAG, TOKEN_PTAG):
                tag_name, tag_attribs, end_tag = self.parse_tag_token(tag_token)
                if end_tag:
                    try:
                        tag = tag_stack.pop()
                    except IndexError:
                        raise_error((b"unexpected close tag '{}'").format(tag_token))

                    if tag_name.lower() != tag.name:
                        raise_error((b"mismatched close tag '{}'").format(tag_name))
                    add_html(tag.render_close(data) or b'')
                else:
                    tag = self.get_tag(tag_name, tag_attribs, data)
                    if tag is None:
                        raise_error((b"unknown tag '{}'").format(tag_name))
                    if not tag.inline:
                        while tag_stack:
                            add_html(tag_stack.pop().render_close(data) or b'')

                    tag_stack.append(tag)
                    add_html(tag.render_open(data) or b'')
                    if tag.auto_close:
                        tag_stack.pop()
                        add_html(tag.render_close(data) or b'')

        while tag_stack:
            tag = tag_stack.pop()
            add_html(tag.render_close(data, text=b'') or b'')

        return (self.cleanup_html((b'').join(html)).strip(), data)

    def __call__(self, text):
        html, data = self.render(text)
        return html

    def __repr__(self):
        return b'<bbcode parser>'

    def __moyafilter__(self, context, app, value, params):
        data = {b'context': context, b'docs': context.get(b'.docs', {}), 
           b'urls': context.get(b'.urls', {})}
        html, data = self.render(value, data=data, path=params.get(b'path', b'unknown'))
        return html

    def __moyacall__(self, params):
        return MoyaFilterParams(self, params)

    def supports_tag(self, name):
        return any(tag.match(name) for tag in self.registry)

    def get_tag(self, tag_name, attribs, data):
        for tag_instance in self.registry:
            if tag_instance.match(tag_name):
                tag_instance.on_insert(attribs, data)
                return tag_instance

        return


parser = BBCode()
add_tag = parser.add_tag
add_tag(InlineTag, b'i', b'<em>', b'</em>')
add_tag(InlineTag, b'b', b'<b>', b'</b>')
add_tag(InlineTag, b'u', b'<u>', b'</u>')
add_tag(InlineTag, b's', b'<s>', b'</s>')
add_tag(TagTag, b'tag')
add_tag(SettingTag, b'setting')
add_tag(InlineCodeTag, b'c')
add_tag(H1Tag, b'h1')
add_tag(H2Tag, b'h2')
add_tag(H3Tag, b'h3')
add_tag(H4Tag, b'h4')
add_tag(URLTag, b'url')
add_tag(RawTag, b'raw')
add_tag(AlertTag, b'alert')
add_tag(AsideTag, b'aside')
add_tag(NoteTag, b'note')
add_tag(IndexTag, b'index')
add_tag(IndexTag, b'appendix')
add_tag(FieldTag, b'title')
add_tag(FieldTag, b'class')
add_tag(FieldTag, b'section')
add_tag(FieldTag, b'name')
add_tag(FieldTag, b'id')
add_tag(CodeTag, b'code')
add_tag(DocTag, b'doc')
add_tag(DocLinkTag, b'link')
add_tag(DefinitionsTag, b'definitions')
add_tag(DefineTag, b'define')
add_tag(BreakTag, b'br')
render = parser
render_console = parser.render_console
if __name__ == b'__main__':
    text = b'This is a [i]test[/i] of [b]bbcode[/b] rendering in the console.\n\n    <echo>${hobbits}</echo>\n\n    '
    text = b'[h1]te]bst[/c]'
    render(text)