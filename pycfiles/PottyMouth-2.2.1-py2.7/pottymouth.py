# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/pottymouth.py
# Compiled at: 2012-09-09 13:18:23
from __future__ import unicode_literals
import re, sys
__version__ = b'2.2.1'
short_line_length = 50
encoding = b'utf8'

class TokenMatcher(object):

    def __init__(self, name, pattern, replace=None):
        self.name = name
        self.pattern = re.compile(pattern, re.IGNORECASE | re.UNICODE)
        self.replace = replace

    def match(self, string):
        return self.pattern.match(string)


protocol_pattern = re.compile(b'^\\w+://', re.IGNORECASE)
domain_pattern = b'([-\\w]+\\.)+\\w\\w+'
_URI_pattern = b'((' + b'(https?|webcal|feed|ftp|news|nntp)://' + b'([-\\w]+(:[-\\w]+)?@)?' + b')|www\\.)' + domain_pattern + b'(:\\d+)?' + b"(/([-\\w$\\.+!*'(),;:@%&=?/~#]*[-\\w$+*(@%&=/~#])?)?"
URI_pattern = _URI_pattern
email_pattern = b'[^()<>@,;:\\"\\[\\]\\s]+@' + domain_pattern
image_pattern = _URI_pattern + b'\\.(jpe?g|png|gif)'
youtube_pattern = b'http://(?:www\\.)?youtube.com/(?:watch\\?)?v=?/?([\\w\\-]{11})'
youtube_matcher = re.compile(youtube_pattern, re.IGNORECASE)
white = b'[ \\t\\xa0\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u202f\u205f\u3000]'
token_order = (
 TokenMatcher(b'NEW_LINE', b'(\\r?\\n)(' + white + b'*)'),
 TokenMatcher(b'YOUTUBE', b'(' + youtube_pattern + b')'),
 TokenMatcher(b'IMAGE', b'(' + image_pattern + b')'),
 TokenMatcher(b'URL', b'(' + URI_pattern + b')'),
 TokenMatcher(b'EMAIL', b'(' + email_pattern + b')'),
 TokenMatcher(b'HASH', b'(' + white + b'*#' + white + b'+)(?=\\S+)'),
 TokenMatcher(b'DASH', b'(' + white + b'*-' + white + b'+)(?=\\S+)'),
 TokenMatcher(b'NUMBERED', b'(' + white + b'*\\d+(\\.\\)?|\\))' + white + b'+)(?=\\S+)'),
 TokenMatcher(b'ITEMSTAR', b'(' + white + b'*\\*' + white + b'+)(?=\\S+)'),
 TokenMatcher(b'BULLET', b'(' + white + b'*•' + white + b'+)(?=\\S+)'),
 TokenMatcher(b'UNDERSCORE', b'(_)'),
 TokenMatcher(b'STAR', b'(\\*)'),
 TokenMatcher(b'RIGHT_ANGLE', b'(>(?:' + white + b'*>)*)(' + white + b'*)'),
 TokenMatcher(b'DEFINITION', b'([^\\n\\:]{2,20}\\:' + white + b'+)(?=\\S+)'),
 TokenMatcher(b'EMDASH', b'(--)', replace=unichr(8212)),
 TokenMatcher(b'ELLIPSIS', b'(\\.\\.\\.)', replace=unichr(8230)))
list_tokens = (
 b'HASH', b'NUMBERED', b'DASH', b'ITEMSTAR', b'BULLET')

class Replacer(object):

    def __init__(self, pattern, replace):
        self.pattern = re.compile(pattern, re.UNICODE)
        self.replace = replace

    def sub(self, string):
        return self.pattern.sub(self.replace, string)


smart_quote_replacers = [
 Replacer(b'(``)', unichr(8220)),
 Replacer(b"('')", unichr(8221)),
 Replacer(b'(\\b"\\b)', unichr(34)),
 Replacer(b"(\\b'\\b)", unichr(8217)),
 Replacer(b'(\\b"\\B)', unichr(8221)),
 Replacer(b'(\\B"\\b)', unichr(8220)),
 Replacer(b"(\\b'\\B)", unichr(8217)),
 Replacer(b"(\\B'\\b)", unichr(8216)),
 Replacer(b'(")(\\s)', unichr(8221) + b'\\2'),
 Replacer(b'(\\s)(")', b'\\1' + unichr(8220)),
 Replacer(b"(')(\\s)", unichr(8217) + b'\\2'),
 Replacer(b"(\\s)(')", b'\\1' + unichr(8216)),
 Replacer(b'(`)', unichr(8216))]

class Token(unicode):

    def __new__(cls, name, content=b''):
        self = unicode.__new__(cls, content)
        return self

    def __init__(self, name, content=b''):
        self.name = name

    def __repr__(self):
        return b'%s{%s}' % (self.name, super(Token, self).__repr__())

    def __add__(self, extra):
        return Token(self.name, super(Token, self).__add__(extra))


def escape(string):
    out = string.replace(b'&', b'&amp;')
    out = out.replace(b'<', b'&lt;')
    out = out.replace(b'>', b'&gt;')
    return out


class Node(list):

    def __init__(self, name, *contents, **kw):
        super(list, self).__init__()
        self.name = name.lower()
        self.extend(contents)
        self._attributes = kw.get(b'attributes', {})

    def node_children(self):
        for n in self:
            if isinstance(n, Node):
                return True

        return False

    def _inner_content(self, strip=True):
        content = b''
        for c in self:
            if isinstance(c, Node):
                new_content = bytes(c)
                if content and (content.endswith(b'>') or new_content.startswith(b'<')):
                    content += b'\n'
                content += new_content
            else:
                if content and content.endswith(b'>'):
                    content += b'\n'
                content += escape(c).encode(encoding, b'xmlcharrefreplace')

        content = content.replace(b'\n', b'\n  ')
        if strip:
            content = content.strip()
        return content

    def __str__(self):
        name = bytes(self.name)
        if self.name in ('br', 'img'):
            return b'<%s%s />' % (name, self._attribute_string())
        else:
            if self.node_children():
                return b'<%s%s>\n  %s\n</%s>' % (name, self._attribute_string(), self._inner_content(), name)
            if self.name == b'span':
                return self._inner_content(strip=False)
            return b'<%s%s>%s</%s>' % (name, self._attribute_string(), self._inner_content(), name)

    def _attribute_string(self):
        content = b''
        if self._attributes:
            for k, v in self._attributes.items():
                content += b' %s="%s"' % (k.encode(encoding), escape(v).encode(encoding, b'xmlcharrefreplace'))

        return content


class URLNode(Node):

    def __init__(self, content, internal=False):
        attributes = {b'href': content}
        if not internal:
            attributes[b'class'] = b'external'
        if content.startswith(b'http://'):
            content = content[7:]
        Node.__init__(self, b'a', content, attributes=attributes)


class LinkNode(URLNode):
    pass


class EmailNode(URLNode):

    def __init__(self, content, internal=False):
        attributes = {b'href': b'mailto:' + content}
        if not internal:
            attributes[b'class'] = b'external'
        Node.__init__(self, b'a', content, attributes=attributes)


class ImageNode(Node):

    def __init__(self, content):
        Node.__init__(self, b'img', b'', attributes={b'src': content})


class YouTubeNode(Node):

    def __init__(self, content):
        Node.__init__(self, b'object', attributes={b'width': b'425', b'height': b'350'})
        ytid = youtube_matcher.match(content).groups()[0]
        url = b'http://www.youtube.com/v/' + ytid
        self.append(Node(name=b'param', attributes={b'name': b'movie', b'value': url}))
        self.append(Node(b'param', attributes={b'name': b'wmode', b'value': b'transparent'}))
        self.append(Node(b'embed', attributes={b'type': b'application/x-shockwave-flash', b'wmode': b'transparent', 
           b'src': url, b'width': b'425', 
           b'height': b'350'}))


class PottyMouth(object):

    def __init__(self, url_check_domains=(), url_white_lists=(), all_links=True, image=True, youtube=True, email=True, all_lists=True, unordered_list=True, ordered_list=True, numbered_list=True, blockquote=True, definition_list=True, bold=True, italic=True, emdash=True, ellipsis=True, smart_quotes=True):
        self._url_check_domain = None
        if url_check_domains:
            self._url_check_domain = re.compile(b'(\\w+://)?((' + (b')|(').join(url_check_domains) + b'))', flags=re.I)
        self._url_white_lists = [ re.compile(w) for w in url_white_lists ]
        self.replacer_list = []
        if smart_quotes:
            self.replacer_list.extend(smart_quote_replacers)
        self.token_list = []
        for t in token_order:
            n = t.name
            if n in ('URL', 'IMAGE', 'YOUTUBE', 'EMAIL') and not all_links:
                continue
            elif n == b'IMAGE' and not image:
                continue
            elif n == b'YOUTUBE' and not youtube:
                continue
            elif n == b'EMAIL' and not email:
                continue
            elif n in ('HASH', 'DASH', 'NUMBERED', 'ITEMSTAR', 'BULLET') and not all_lists:
                continue
            elif n in ('DASH', 'ITEMSTAR', 'BULLET') and not unordered_list:
                continue
            elif n in ('HASH', 'NUMBERED') and not ordered_list:
                continue
            elif n == b'DEFINITION' and not definition_list:
                continue
            elif n == b'NUMBERED' and not numbered_list:
                continue
            elif n == b'STAR' and not bold:
                continue
            elif n == b'UNDERSCORE' and not italic:
                continue
            elif n == b'RIGHT_ANGLE' and not blockquote:
                continue
            elif n == b'EMDASH' and not emdash:
                continue
            elif n == b'ELLIPSIS' and not ellipsis:
                continue
            self.token_list.append(t)

        return

    def pre_replace(self, string):
        for r in self.replacer_list:
            string = r.sub(string)

        return string

    def tokenize(self, string):
        p = 0
        found_tokens = []
        unmatched_collection = b''
        while p < len(string):
            found_token = False
            for tm in self.token_list:
                m = tm.match(string[p:])
                if m:
                    found_token = True
                    content = m.groups()[0]
                    p += len(content)
                    if tm.replace is not None:
                        unmatched_collection += tm.replace
                        break
                    if unmatched_collection:
                        found_tokens.append(Token(b'TEXT', unmatched_collection))
                    unmatched_collection = b''
                    if tm.name == b'NEW_LINE':
                        if found_tokens and found_tokens[(-1)].name == b'TEXT':
                            found_tokens[(-1)] += b' '
                        content = b' '
                    found_tokens.append(Token(tm.name, content))
                    if tm.name in ('NEW_LINE', 'RIGHT_ANGLE') and m.groups()[1]:
                        found_tokens.append(Token(b'INDENT', m.groups()[1]))
                        p += len(m.groups()[1])
                    break

            if not found_token:
                unmatched_collection += string[p]
                p += 1

        if unmatched_collection:
            found_tokens.append(Token(b'TEXT', unmatched_collection))
        return found_tokens

    def handle_url(self, t):
        if not protocol_pattern.match(t):
            t = Token(t.name, b'http://' + t)
        if self._url_check_domain and self._url_check_domain.findall(t):
            for w in self._url_white_lists:
                if w.match(t):
                    return LinkNode(t, internal=True)

            return Node(b'span', t)
        else:
            return LinkNode(t)

    def parse_atomics(self, tokens):
        collect = []
        while tokens:
            t = tokens[0]
            if t.name == b'TEXT':
                t = tokens.pop(0)
                if t:
                    collect.append(Node(b'span', t))
            elif t.name == b'URL':
                collect.append(self.handle_url(tokens.pop(0)))
            elif t.name == b'IMAGE':
                collect.append(ImageNode(tokens.pop(0)))
            elif t.name == b'EMAIL':
                collect.append(EmailNode(tokens.pop(0)))
            elif t.name == b'YOUTUBE':
                collect.append(YouTubeNode(tokens.pop(0)))
            elif t.name == b'RIGHT_ANGLE':
                collect.append(Node(b'span', tokens.pop(0)))
            elif t.name == b'DEFINITION':
                collect.append(Node(b'span', tokens.pop(0)))
            elif t.name in list_tokens and t.name != b'ITEMSTAR':
                collect.append(Node(b'span', tokens.pop(0)))
            else:
                break

        return collect

    def parse_italic(self, tokens, inner=False):
        t = tokens.pop(0)
        assert t.name == b'UNDERSCORE'
        collect = []
        while tokens:
            atomics = self.parse_atomics(tokens)
            if atomics:
                collect.extend(atomics)
            elif not inner and (tokens[0].name == b'STAR' or tokens[0].name == b'ITEMSTAR'):
                collect.extend(self.parse_bold(tokens, inner=True))
            elif tokens[0].name == b'UNDERSCORE':
                t = tokens.pop(0)
                if collect:
                    newi = Node(b'i')
                    newi.extend(collect)
                    return [
                     newi]
                return [t * 2]
            else:
                break

        return [
         Node(b'span', b'_')] + collect

    def parse_bold(self, tokens, inner=False):
        t = tokens.pop(0)
        assert t.name == b'STAR' or t.name == b'ITEMSTAR'
        collect = []
        while tokens:
            atomics = self.parse_atomics(tokens)
            if atomics:
                collect.extend(atomics)
            elif not inner and tokens[0].name == b'UNDERSCORE':
                collect.extend(self.parse_italic(tokens, inner=True))
            elif tokens[0].name == b'STAR' or tokens[0].name == b'ITEMSTAR':
                t = tokens.pop(0)
                if collect:
                    newb = Node(b'b')
                    newb.extend(collect)
                    return [
                     newb]
                return [t * 2]
            else:
                break

        return [
         Node(b'span', b'*')] + collect

    def parse_line(self, tokens):
        collect = []
        while tokens:
            atomics = self.parse_atomics(tokens)
            if atomics:
                collect.extend(atomics)
            if not tokens:
                break
            elif tokens[0].name == b'UNDERSCORE':
                collect.extend(self.parse_italic(tokens))
            elif tokens[0].name == b'STAR' or tokens[0].name == b'ITEMSTAR':
                collect.extend(self.parse_bold(tokens))
            else:
                break

        return collect

    def parse_list(self, tokens):
        initial_indent = 0
        if tokens[0].name == b'INDENT':
            initial_indent = len(tokens[0])
            tokens.pop(0)
        t = tokens[0]
        assert t.name in list_tokens
        if t.name == b'HASH' or t.name == b'NUMBERED':
            l = Node(b'ol')
        else:
            if t.name == b'DASH' or t.name == b'ITEMSTAR' or t.name == b'BULLET':
                l = Node(b'ul')
            while tokens:
                t = tokens[0]
                if t.name in list_tokens:
                    tokens.pop(0)
                    i = Node(b'li')
                    i.extend(self.parse_line(tokens))
                    l.append(i)
                elif t.name == b'INDENT':
                    tokens.pop(0)
                    if len(t) > initial_indent:
                        if tokens and tokens[0].name not in list_tokens:
                            l[(-1)].extend(self.parse_line(tokens))
                elif t.name == b'NEW_LINE':
                    tokens.pop(0)
                    if tokens and tokens[0].name not in list_tokens and tokens[0].name != b'INDENT':
                        break
                else:
                    break

        return [
         l]

    def parse_definition(self, tokens):
        initial_indent = 0
        if tokens[0].name == b'INDENT':
            initial_indent = len(tokens[0])
            tokens.pop(0)
        assert tokens[0].name == b'DEFINITION'
        dl = Node(b'dl')
        while tokens:
            t = tokens[0]
            if t.name == b'DEFINITION':
                dt = tokens.pop(0)
                dl.append(Node(b'dt', dt))
                dd = Node(b'dd')
                dd.extend(self.parse_line(tokens))
                dl.append(dd)
            elif t.name == b'INDENT':
                tokens.pop(0)
                if len(t) > initial_indent:
                    if tokens and tokens[0].name != b'DEFINITION':
                        dl[(-1)].extend(self.parse_line(tokens))
            elif t.name == b'NEW_LINE':
                tokens.pop(0)
                if tokens and tokens[0].name not in ('DEFINITION', 'INDENT'):
                    break
            else:
                break

        return [
         dl]

    def parse_quote(self, tokens):
        initial_indent = 0
        if tokens[0].name == b'INDENT':
            initial_indent = len(tokens[0])
            tokens.pop(0)
        assert tokens[0].name == b'RIGHT_ANGLE'
        quote = Node(b'blockquote')
        new_tokens = []

        def handle_quote(token):
            """Strip a single > off of a RIGHT_ANGLE token, effectively decreasing the quoting level"""
            new_angle = token.replace(b'>', b'', 1).strip()
            if new_angle:
                new_tokens.append(Token(b'RIGHT_ANGLE', new_angle))

        handle_quote(tokens.pop(0))
        while tokens:
            if tokens[0].name == b'NEW_LINE':
                new_tokens.append(tokens.pop(0))
                if tokens and tokens[0].name == b'INDENT':
                    t = tokens.pop(0)
                    if len(t) > initial_indent:
                        break
                if tokens:
                    if tokens[0].name == b'RIGHT_ANGLE':
                        handle_quote(tokens.pop(0))
                    else:
                        break
            else:
                new_tokens.append(tokens.pop(0))

        quote.extend(self.parse_blocks(new_tokens))
        return [quote]

    def calculate_line_length(self, line):
        length = 0
        for i in line:
            if isinstance(i, list):
                length += self.calculate_line_length(i)
            elif isinstance(i, unicode):
                length += len(i)
            else:
                raise TypeError(b"Don't know what to do with line element of type %r" % type(i))

        return length

    def parse_paragraph(self, tokens):
        p = Node(b'p')
        shorts = []

        def parse_shorts(shorts, line=None):
            collect = []
            if len(shorts) >= 2:
                if p:
                    collect.append(Node(b'br'))
                collect.extend(shorts.pop(0))
                while shorts:
                    collect.append(Node(b'br'))
                    collect.extend(shorts.pop(0))

                if line:
                    collect.append(Node(b'br'))
            else:
                while shorts:
                    collect.extend(shorts.pop(0))

            return collect

        while tokens:
            t = tokens[0]
            if t.name == b'NEW_LINE' or t.name == b'INDENT':
                tokens.pop(0)
                if tokens and tokens[0].name == b'NEW_LINE':
                    tokens.pop(0)
                    break
                elif tokens and tokens[0].name in ('RIGHT_ANGLE', 'DEFINITION') + list_tokens:
                    if t.name == b'INDENT':
                        tokens.insert(0, t)
                    break
            else:
                line = self.parse_line(tokens)
                if self.calculate_line_length(line) < short_line_length:
                    shorts.append(line)
                else:
                    p.extend(parse_shorts(shorts, line))
                    p.extend(line)

        p.extend(parse_shorts(shorts))
        if p:
            return [p]
        else:
            return []
            return

    def parse_blocks(self, tokens):
        collect = []
        while tokens:
            t = tokens[0]
            if t.name == b'NEW_LINE':
                tokens.pop(0)
                continue
            if t.name == b'INDENT':
                if len(tokens) == 1:
                    break
                t = tokens[1]
            if t.name == b'RIGHT_ANGLE':
                collect.extend(self.parse_quote(tokens))
            elif t.name in list_tokens:
                collect.extend(self.parse_list(tokens))
            elif t.name == b'DEFINITION':
                collect.extend(self.parse_definition(tokens))
            else:
                collect.extend(self.parse_paragraph(tokens))

        return collect

    def parse(self, s):
        if isinstance(s, bytes):
            s = s.decode(encoding)
        assert isinstance(s, unicode), b'PottyMouth input must be unicode or bytes types'
        s = self.pre_replace(s)
        tokens = self.tokenize(s)
        finished = self.parse_blocks(tokens)
        return finished


if __name__ == b'__main__':

    def parse_and_print(w, text):
        blocks = w.parse(text)
        for b in blocks:
            print b


    w = PottyMouth(url_check_domains=(b'www.mysite.com', b'mysite.com'), url_white_lists=(
     b'https?://www\\.mysite\\.com/allowed/url\\?id=\\d+',))
    if not sys.stdin.isatty():
        parse_and_print(w, sys.stdin.read())
        raise SystemExit(0)
    else:
        if len(sys.argv) >= 2:
            for i, filename in enumerate(sys.argv[1:]):
                if i:
                    print b'=' * 70
                fileobj = open(filename, b'r')
                text = fileobj.read()
                fileobj.close()
                parse_and_print(w, text)

            raise SystemExit(0)
        EOF_DESCRIPTION = b'Ctrl-D'
        if sys.platform == b'win32':
            EOF_DESCRIPTION = b'Ctrl-Z'
        while True:
            print b'input (end with %s)>>' % EOF_DESCRIPTION
            try:
                text = sys.stdin.read()
            except KeyboardInterrupt:
                break

            if text:
                parse_and_print(w, text)
            else:
                sys.stdin.seek(1)