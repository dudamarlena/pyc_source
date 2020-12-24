# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-i386/egg/sleepy/markdown2.py
# Compiled at: 2011-05-07 17:23:22
r"""A fast and complete Python implementation of Markdown.

[from http://daringfireball.net/projects/markdown/]
> Markdown is a text-to-HTML filter; it translates an easy-to-read /
> easy-to-write structured text format into HTML.  Markdown's text
> format is most similar to that of plain text email, and supports
> features such as headers, *emphasis*, code blocks, blockquotes, and
> links.
>
> Markdown's syntax is designed not as a generic markup language, but
> specifically to serve as a front-end to (X)HTML. You can use span-level
> HTML tags anywhere in a Markdown document, and you can use block level
> HTML tags (like <div> and <table> as well).

Module usage:

    >>> import markdown2
    >>> markdown2.markdown("*boo!*")  # or use `html = markdown_path(PATH)`
    u'<p><em>boo!</em></p>\n'

    >>> markdowner = Markdown()
    >>> markdowner.convert("*boo!*")
    u'<p><em>boo!</em></p>\n'
    >>> markdowner.convert("**boom!**")
    u'<p><strong>boom!</strong></p>\n'

This implementation of Markdown implements the full "core" syntax plus a
number of extras (e.g., code syntax coloring, footnotes) as described on
<http://code.google.com/p/python-markdown2/wiki/Extras>.
"""
cmdln_desc = 'A fast and complete Python implementation of Markdown, a\ntext-to-HTML conversion tool for web writers.\n\nSupported extras (see -x|--extras option below):\n* code-friendly: Disable _ and __ for em and strong.\n* code-color: Pygments-based syntax coloring of <code> sections.\n* cuddled-lists: Allow lists to be cuddled to the preceding paragraph.\n* footnotes: Support footnotes as in use on daringfireball.net and\n  implemented in other Markdown processors (tho not in Markdown.pl v1.0.1).\n* header-ids: Adds "id" attributes to headers. The id value is a slug of\n  the header text.\n* html-classes: Takes a dict mapping html tag names (lowercase) to a\n  string to use for a "class" tag attribute. Currently only supports\n  "pre" and "code" tags. Add an issue if you require this for other tags.\n* markdown-in-html: Allow the use of `markdown="1"` in a block HTML tag to\n  have markdown processing be done on its contents. Similar to\n  <http://michelf.com/projects/php-markdown/extra/#markdown-attr> but with\n  some limitations.\n* pyshell: Treats unindented Python interactive shell sessions as <code>\n  blocks.\n* link-patterns: Auto-link given regex patterns in text (e.g. bug number\n  references, revision number references).\n* smarty-pants: Replaces \' and " with curly quotation marks or curly \n  apostrophes.  Replaces --, ---, ..., and . . . with en dashes, em dashes, \n  and ellipses.\n* toc: The returned HTML string gets a new "toc_html" attribute which is\n  a Table of Contents for the document. (experimental)\n* xml: Passes one-liner processing instructions and namespaced XML tags.\n'
__version_info__ = (
 1, 0, 1, 18)
__version__ = '1.0.1.18'
__author__ = 'Trent Mick'
import os, sys
from pprint import pprint
import re, logging
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

import optparse
from random import random, randint
import codecs
from urllib import quote
from sleepy.shorties import to_url, dictize, s, unixy, detab, _blank_line_re
from webhelpers.html import tags, literal
if sys.version_info[:2] < (2, 4):
    from sets import Set as set

    def reversed(sequence):
        for i in sequence[::-1]:
            yield i


    def _unicode_decode(s, encoding, errors='xmlcharrefreplace'):
        return unicode(s, encoding, errors)


else:

    def _unicode_decode(s, encoding, errors='strict'):
        return s.decode(encoding, errors)


DEBUG = True
log = logging.getLogger('markdown')
if not logging.root.handlers:
    logging.basicConfig()
log.setLevel(logging.DEBUG)
DEFAULT_TAB_WIDTH = 4
try:
    import uuid
except ImportError:
    SECRET_SALT = str(randint(0, 1000000))
else:
    SECRET_SALT = str(uuid.uuid4())

def _hash_ascii(s):
    return 'md5-' + md5(SECRET_SALT + s).hexdigest()


def _hash_text(s):
    return 'md5-' + md5(SECRET_SALT + s.encode('utf-8')).hexdigest()


g_escape_table = dict([ (ch, _hash_ascii(ch)) for ch in '\\`*_{}[]()>#+-.!'
                      ])

class MarkdownError(Exception):
    pass


def markdown_path(path, encoding='utf-8', html4tags=False, tab_width=DEFAULT_TAB_WIDTH, safe_mode=None, extras=None, link_patterns=None, use_file_vars=False, inline=False, p_class=None):
    fp = codecs.open(path, 'r', encoding)
    text = fp.read()
    fp.close()
    return Markdown(html4tags=html4tags, tab_width=tab_width, safe_mode=safe_mode, extras=extras, link_patterns=link_patterns, use_file_vars=use_file_vars, inline=inline, p_class=p_class).convert(text)


def markdown(text, html4tags=False, tab_width=DEFAULT_TAB_WIDTH, safe_mode=None, extras=None, link_patterns=None, use_file_vars=False, inline=False, p_class=None):
    return Markdown(html4tags=html4tags, tab_width=tab_width, safe_mode=safe_mode, extras=extras, link_patterns=link_patterns, use_file_vars=use_file_vars, inline=inline, p_class=p_class).convert(text)


class Markdown(object):
    extras = None
    urls = None
    titles = None
    html_blocks = None
    html_spans = None
    html_removed_text = '[HTML_REMOVED]'
    list_level = 0

    def __init__(self, html4tags=False, tab_width=DEFAULT_TAB_WIDTH, safe_mode=None, extras=None, link_patterns=None, use_file_vars=False, inline=False, p_class=None):
        if html4tags:
            self.empty_element_suffix = '>'
        else:
            self.empty_element_suffix = ' />'
        self.tab_width = tab_width
        self.inline = inline
        self.p_class = tags.css_classes(p_class or (
         (
          'markdown',
          True),))
        if safe_mode is True:
            self.safe_mode = 'replace'
        else:
            self.safe_mode = safe_mode
        self.extras = dictize(self.extras)
        self.extras.update(dictize(extras))
        if 'toc' in self.extras:
            self.extras.setdefault('header-ids')
        self._instance_extras = self.extras.copy()
        self.link_patterns = link_patterns
        self.use_file_vars = use_file_vars
        self._outdent_re = re.compile(s(' ^( \\t\n                                                   | [ ] {1,{{ tab_width }}}\n                                                )', tab_width=tab_width), re.M | re.X)
        self._escape_table = g_escape_table.copy()
        if 'smarty-pants' in self.extras:
            self._escape_table['"'] = _hash_ascii('"')
            self._escape_table["'"] = _hash_ascii("'")

    def reset(self):
        self.urls = {}
        self.titles = {}
        self.html_blocks = {}
        self.html_spans = {}
        self.list_level = 0
        self.extras = self._instance_extras.copy()
        if 'footnotes' in self.extras:
            self.footnotes = {}
            self.footnote_ids = []
        if 'header-ids' in self.extras:
            self._count_from_header_id = {}

    def convert(self, text):
        """Convert the given text."""
        self.reset()
        if not isinstance(text, unicode):
            text = unicode(text, 'utf-8')
        if self.use_file_vars:
            emacs_vars = self._get_emacs_vars(text)
            if 'markdown-extras' in emacs_vars:
                splitter = re.compile('[ ,]+')
                for e in splitter.split(emacs_vars['markdown-extras']):
                    if '=' in e:
                        (ename, earg) = e.split('=', 1)
                        try:
                            earg = int(earg)
                        except ValueError:
                            pass

                    else:
                        ename, earg = e, None
                    self.extras[ename] = earg

        text = unixy(text)
        text += '\n\n'
        text = self._detab(text)
        text = _blank_line_re.sub('', text)
        if self.safe_mode:
            text = self._hash_html_spans(text)
        text = self._hash_html_blocks(text, raw=True)
        if 'footnotes' in self.extras:
            text = self._strip_footnote_definitions(text)
        text = self._strip_link_definitions(text)
        text = self._run_block_gamut(text)
        if 'footnotes' in self.extras:
            text = self._add_footnotes(text)
        text = self.postprocess(text)
        text = self._unescape_special_chars(text)
        if self.safe_mode:
            text = self._unhash_html_spans(text)
        if not self.inline:
            text += '\n'
        rv = UnicodeWithAttrs(text)
        if 'toc' in self.extras:
            rv._toc = self._toc
        return rv

    def postprocess(self, text):
        """A hook for subclasses to do some postprocessing of the html, if
        desired. This is called before unescaping of special chars and
        unhashing of raw HTML spans.
        """
        return text

    _emacs_oneliner_vars_pat = re.compile('-\\*-\\s*([^\\r\\n]*?)\\s*-\\*-', re.UNICODE)
    _emacs_local_vars_pat = re.compile('^\n        (?P<prefix>(?:[^\\r\\n|\\n|\\r])*?)\n        [\\ \\t]*Local\\ Variables:[\\ \\t]*\n        (?P<suffix>.*?)(?:\\r\\n|\\n|\\r)\n        (?P<content>.*?\\1End:)\n        ', re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE)

    def _get_emacs_vars(self, text):
        """Return a dictionary of emacs-style local variables.

        Parsing is done loosely according to this spec (and according to
        some in-practice deviations from this):
        http://www.gnu.org/software/emacs/manual/html_node/emacs/Specifying-File-Variables.html#Specifying-File-Variables
        """
        emacs_vars = {}
        SIZE = pow(2, 13)
        head = text[:SIZE]
        if '-*-' in head:
            match = self._emacs_oneliner_vars_pat.search(head)
            if match:
                emacs_vars_str = match.group(1)
                assert '\n' not in emacs_vars_str
                emacs_var_strs = [ s.strip() for s in emacs_vars_str.split(';') if s.strip()
                                 ]
                if len(emacs_var_strs) == 1 and ':' not in emacs_var_strs[0]:
                    emacs_vars['mode'] = emacs_var_strs[0].strip()
                else:
                    for emacs_var_str in emacs_var_strs:
                        try:
                            (variable, value) = emacs_var_str.strip().split(':', 1)
                        except ValueError:
                            log.debug('emacs variables error: malformed -*- line: %r', emacs_var_str)
                            continue

                        emacs_vars[variable.lower()] = value.strip()

        tail = text[-SIZE:]
        if 'Local Variables' in tail:
            match = self._emacs_local_vars_pat.search(tail)
            if match:
                prefix = match.group('prefix')
                suffix = match.group('suffix')
                lines = match.group('content').splitlines(0)
                for (i, line) in enumerate(lines):
                    if not line.startswith(prefix):
                        log.debug("emacs variables error: line '%s' does not use proper prefix '%s'" % (
                         line, prefix))
                        return {}
                    if i != len(lines) - 1 and not line.endswith(suffix):
                        log.debug("emacs variables error: line '%s' does not use proper suffix '%s'" % (
                         line, suffix))
                        return {}

                continued_for = None
                for line in lines[:-1]:
                    if prefix:
                        line = line[len(prefix):]
                    if suffix:
                        line = line[:-len(suffix)]
                    line = line.strip()
                    if continued_for:
                        variable = continued_for
                        if line.endswith('\\'):
                            line = line[:-1].rstrip()
                        else:
                            continued_for = None
                        emacs_vars[variable] += ' ' + line
                    else:
                        try:
                            (variable, value) = line.split(':', 1)
                        except ValueError:
                            log.debug("local variables error: missing colon in local variables entry: '%s'" % line)
                            continue

                        value = value.strip()
                        if value.endswith('\\'):
                            value = value[:-1].rstrip()
                            continued_for = variable
                        else:
                            continued_for = None
                        emacs_vars[variable] = value

        for (var, val) in emacs_vars.items():
            if len(val) > 1 and (val.startswith('"') and val.endswith('"') or val.startswith('"') and val.endswith('"')):
                emacs_vars[var] = val[1:-1]

        return emacs_vars

    def _detab(self, text):
        r"""Remove (leading?) tabs from a file.

            >>> m = Markdown()
            >>> m._detab("\tfoo")
            '    foo'
            >>> m._detab("  \tfoo")
            '    foo'
            >>> m._detab("\t  foo")
            '      foo'
            >>> m._detab("  foo")
            '  foo'
            >>> m._detab("  foo\n\tbar\tblam")
            '  foo\n    bar blam'
        """
        return detab(text, tab_width=self.tab_width)

    _html5tags = '|article|aside|header|hgroup|footer|nav|section|figure|figcaption'
    _block_tags_a = 'p|div|h[1-6]|blockquote|pre|table|dl|ol|ul|script|noscript|form|fieldset|iframe|math|ins|del'
    _block_tags_a += _html5tags
    _strict_tag_block_re = re.compile('\n        (                       # save in \\1\n            ^                   # start of line  (with re.M)\n            <(%s)               # start tag = \\2\n            \\b                  # word break\n            (.*\\n)*?            # any number of lines, minimally matching\n            </\\2>               # the matching end tag\n            [ \\t]*              # trailing spaces/tabs\n            (?=\\n+|\\Z)          # followed by a newline or end of document\n        )\n        ' % _block_tags_a, re.X | re.M)
    _block_tags_b = 'p|div|h[1-6]|blockquote|pre|table|dl|ol|ul|script|noscript|form|fieldset|iframe|math'
    _block_tags_b += _html5tags
    _liberal_tag_block_re = re.compile('\n        (                       # save in \\1\n            ^                   # start of line  (with re.M)\n            <(%s)               # start tag = \\2\n            \\b                  # word break\n            (.*\\n)*?            # any number of lines, minimally matching\n            .*</\\2>             # the matching end tag\n            [ \\t]*              # trailing spaces/tabs\n            (?=\\n+|\\Z)          # followed by a newline or end of document\n        )\n        ' % _block_tags_b, re.X | re.M)
    _html_markdown_attr_re = re.compile('\\s+markdown=("1"|\'1\')')

    def _hash_html_block_sub(self, match, raw=False):
        html = match.group(1)
        if raw and self.safe_mode:
            html = self._sanitize_html(html)
        elif 'markdown-in-html' in self.extras and 'markdown=' in html:
            first_line = html.split('\n', 1)[0]
            m = self._html_markdown_attr_re.search(first_line)
            if m:
                lines = html.split('\n')
                middle = ('\n').join(lines[1:-1])
                last_line = lines[(-1)]
                first_line = first_line[:m.start()] + first_line[m.end():]
                f_key = _hash_text(first_line)
                self.html_blocks[f_key] = first_line
                l_key = _hash_text(last_line)
                self.html_blocks[l_key] = last_line
                return ('').join(['\n\n', f_key,
                 '\n\n', middle, '\n\n',
                 l_key, '\n\n'])
        key = _hash_text(html)
        self.html_blocks[key] = html
        return '\n\n' + key + '\n\n'

    def _hash_html_blocks(self, text, raw=False):
        """Hashify HTML blocks

        We only want to do this for block-level HTML tags, such as headers,
        lists, and tables. That's because we still want to wrap <p>s around
        "paragraphs" that are wrapped in non-block-level tags, such as anchors,
        phrase emphasis, and spans. The list of tags we're looking for is
        hard-coded.

        @param raw {boolean} indicates if these are raw HTML blocks in
            the original source. It makes a difference in "safe" mode.
        """
        if '<' not in text:
            return text
        hash_html_block_sub = _curry(self._hash_html_block_sub, raw=raw)
        text = self._strict_tag_block_re.sub(hash_html_block_sub, text)
        text = self._liberal_tag_block_re.sub(hash_html_block_sub, text)
        if '<hr' in text:
            _hr_tag_re = _hr_tag_re_from_tab_width(self.tab_width)
            text = _hr_tag_re.sub(hash_html_block_sub, text)
        if '<!--' in text:
            start = 0
            while True:
                try:
                    start_idx = text.index('<!--', start)
                except ValueError, ex:
                    break

                try:
                    end_idx = text.index('-->', start_idx) + 3
                except ValueError, ex:
                    break

                start = end_idx
                if start_idx:
                    for i in range(self.tab_width - 1):
                        if text[(start_idx - 1)] != ' ':
                            break
                        start_idx -= 1
                        if start_idx == 0:
                            break

                    if start_idx == 0:
                        pass
                    elif start_idx == 1 and text[0] == '\n':
                        start_idx = 0
                    elif text[start_idx - 2:start_idx] == '\n\n':
                        pass
                    else:
                        break
                while end_idx < len(text):
                    if text[end_idx] not in ' \t':
                        break
                    end_idx += 1

                if text[end_idx:end_idx + 2] not in ('', '\n', '\n\n'):
                    continue
                html = text[start_idx:end_idx]
                if raw and self.safe_mode:
                    html = self._sanitize_html(html)
                key = _hash_text(html)
                self.html_blocks[key] = html
                text = text[:start_idx] + '\n\n' + key + '\n\n' + text[end_idx:]

        if 'xml' in self.extras:
            _xml_oneliner_re = _xml_oneliner_re_from_tab_width(self.tab_width)
            text = _xml_oneliner_re.sub(hash_html_block_sub, text)
        return text

    def _strip_link_definitions(self, text):
        less_than_tab = self.tab_width - 1
        _link_def_re = re.compile('\n            ^[ ]{0,%d}\\[(.+)\\]: # id = \\1\n              [ \\t]*\n              \\n?               # maybe *one* newline\n              [ \\t]*\n            <?(.+?)>?           # url = \\2\n              [ \\t]*\n            (?:\n                \\n?             # maybe one newline\n                [ \\t]*\n                (?<=\\s)         # lookbehind for whitespace\n                [\'"(]\n                ([^\\n]*)        # title = \\3\n                [\'")]\n                [ \\t]*\n            )?  # title is optional\n            (?:\\n+|\\Z)\n            ' % less_than_tab, re.X | re.M | re.U)
        return _link_def_re.sub(self._extract_link_def_sub, text)

    def _extract_link_def_sub(self, match):
        (id, url, title) = match.groups()
        key = id.lower()
        self.urls[key] = self._encode_amps_and_angles(url)
        if title:
            self.titles[key] = title
        return ''

    def _extract_footnote_def_sub(self, match):
        (id, text) = match.groups()
        text = _dedent(text, skip_first_line=not text.startswith('\n')).strip()
        normed_id = re.sub('\\W', '-', id)
        self.footnotes[normed_id] = text + '\n\n'
        return ''

    def _strip_footnote_definitions(self, text):
        """A footnote definition looks like this:

            [^note-id]: Text of the note.

                May include one or more indented paragraphs.

        Where,
        - The 'note-id' can be pretty much anything, though typically it
          is the number of the footnote.
        - The first paragraph may start on the next line, like so:
            
            [^note-id]:
                Text of the note.
        """
        less_than_tab = self.tab_width - 1
        footnote_def_re = re.compile('\n            ^[ ]{0,%d}\\[\\^(.+)\\]:   # id = \\1\n            [ \\t]*\n            (                       # footnote text = \\2\n              # First line need not start with the spaces.\n              (?:\\s*.*\\n+)\n              (?:\n                (?:[ ]{%d} | \\t)  # Subsequent lines must be indented.\n                .*\\n+\n              )*\n            )\n            # Lookahead for non-space at line-start, or end of doc.\n            (?:(?=^[ ]{0,%d}\\S)|\\Z)\n            ' % (less_than_tab, self.tab_width, self.tab_width), re.X | re.M)
        return footnote_def_re.sub(self._extract_footnote_def_sub, text)

    _hr_data = [
     (
      '*', re.compile('^[ ]{0,3}\\*(.*?)$', re.M)),
     (
      '-', re.compile('^[ ]{0,3}\\-(.*?)$', re.M)),
     (
      '_', re.compile('^[ ]{0,3}\\_(.*?)$', re.M))]

    def _run_block_gamut(self, text):
        text = self._do_headers(text)
        hr = '\n<hr' + self.empty_element_suffix + '\n'
        for (ch, regex) in self._hr_data:
            if ch in text:
                for m in reversed(list(regex.finditer(text))):
                    tail = m.group(1).rstrip()
                    if not tail.strip(ch + ' ') and tail.count('   ') == 0:
                        (start, end) = m.span()
                        text = text[:start] + hr + text[end:]

        text = self._do_lists(text)
        if 'pyshell' in self.extras:
            text = self._prepare_pyshell_blocks(text)
        text = self._do_code_blocks(text)
        text = self._do_block_quotes(text)
        text = self._hash_html_blocks(text)
        text = self._form_paragraphs(text)
        return text

    def _pyshell_block_sub(self, match):
        lines = match.group(0).splitlines(0)
        _dedentlines(lines)
        indent = ' ' * self.tab_width
        s = '\n' + indent + ('\n' + indent).join(lines) + '\n\n'
        return s

    def _prepare_pyshell_blocks(self, text):
        """Ensure that Python interactive shell sessions are put in
        code blocks -- even if not properly indented.
        """
        if '>>>' not in text:
            return text
        less_than_tab = self.tab_width - 1
        _pyshell_block_re = re.compile('\n            ^([ ]{0,%d})>>>[ ].*\\n   # first line\n            ^(\\1.*\\S+.*\\n)*         # any number of subsequent lines\n            ^\\n                     # ends with a blank line\n            ' % less_than_tab, re.M | re.X)
        return _pyshell_block_re.sub(self._pyshell_block_sub, text)

    def _run_span_gamut(self, text):
        text = self._do_code_spans(text)
        text = self._escape_special_chars(text)
        text = self._do_links(text)
        if 'link-patterns' in self.extras:
            text = self._do_link_patterns(text)
        text = self._encode_amps_and_angles(text)
        text = self._do_italics_and_bold(text)
        if 'smarty-pants' in self.extras:
            text = self._do_smart_punctuation(text)
        text = re.sub(' {2,}\\n', ' <br%s\n' % self.empty_element_suffix, text)
        return text

    _sorta_html_tokenize_re = re.compile('\n          (\n            <\n            / ?\n            \\w +\n            (?:\n             \\s +\n             (?:\n              [\\w-] +\n              :\n             ) ?\n             [\\w-] + \n             =\n             (?:\n              "\n              . *?\n              "\n               | \'\n                 . *?\n                 \'\n             )\n            ) *\n            \\s *\n            / ?\n            >\n             | <!--\n               . *?\n               -->\n             | <\\?\n               . *?\n               \\?>\n          )\n         ', re.X)

    def _escape_special_chars(self, text):
        escaped = []
        is_html_markup = False
        for token in self._sorta_html_tokenize_re.split(text):
            if is_html_markup:
                escaped.append(token.replace('*', self._escape_table['*']).replace('_', self._escape_table['_']))
            else:
                escaped.append(self._encode_backslash_escapes(token))
            is_html_markup = not is_html_markup

        return ('').join(escaped)

    def _hash_html_spans(self, text):
        tokens = []
        is_html_markup = False
        for token in self._sorta_html_tokenize_re.split(text):
            if is_html_markup:
                sanitized = self._sanitize_html(token)
                key = _hash_text(sanitized)
                self.html_spans[key] = sanitized
                tokens.append(key)
            else:
                tokens.append(token)
            is_html_markup = not is_html_markup

        return ('').join(tokens)

    def _unhash_html_spans(self, text):
        for (key, sanitized) in self.html_spans.items():
            text = text.replace(key, sanitized)

        return text

    def _sanitize_html(self, s):
        if self.safe_mode == 'replace':
            return self.html_removed_text
        if self.safe_mode == 'escape':
            replacements = [('&', '&amp;'),
             ('<', '&lt;'),
             ('>', '&gt;')]
            for (before, after) in replacements:
                s = s.replace(before, after)

            return s
        raise MarkdownError("invalid value for 'safe_mode': %r (must be 'escape' or 'replace')" % self.safe_mode)

    _tail_of_inline_link_re = re.compile('\n          # Match tail of: [text](/url/) or [text](/url/ "title")\n          \\(            # literal paren\n            [ \\t]*\n            (?P<url>            # \\1\n                <.*?>\n                |\n                .*?\n            )\n            [ \\t]*\n            (                   # \\2\n              ([\'"])            # quote char = \\3\n              (?P<title>.*?)\n              \\3                # matching quote\n            )?                  # title is optional\n          \\)\n        ', re.X | re.S)
    _tail_of_reference_link_re = re.compile('\n          # Match tail of: [text][id]\n          [ ]?          # one optional space\n          (?:\\n[ ]*)?   # one optional newline followed by spaces\n          \\[\n            (?P<id>.*?)\n          \\]\n        ', re.X | re.S)

    def _do_links--- This code section failed: ---

 L. 955         0  LOAD_CONST               3000
                3  STORE_FAST            2  'MAX_LINK_TEXT_SENTINEL'

 L. 960         6  LOAD_CONST               0
                9  STORE_FAST            3  'anchor_allowed_pos'

 L. 962        12  LOAD_CONST               0
               15  STORE_FAST            4  'curr_pos'

 L. 963        18  SETUP_LOOP         1428  'to 1449'
               21  LOAD_GLOBAL           0  'True'
               24  JUMP_IF_FALSE      1420  'to 1447'
               27  POP_TOP          

 L. 979        28  SETUP_EXCEPT         22  'to 53'

 L. 980        31  LOAD_FAST             1  'text'
               34  LOAD_ATTR             1  'index'
               37  LOAD_CONST               '['
               40  LOAD_FAST             4  'curr_pos'
               43  CALL_FUNCTION_2       2  None
               46  STORE_FAST            5  'start_idx'
               49  POP_BLOCK        
               50  JUMP_FORWARD         20  'to 73'
             53_0  COME_FROM            28  '28'

 L. 981        53  DUP_TOP          
               54  LOAD_GLOBAL           2  'ValueError'
               57  COMPARE_OP           10  exception-match
               60  JUMP_IF_FALSE         8  'to 71'
               63  POP_TOP          
               64  POP_TOP          
               65  POP_TOP          
               66  POP_TOP          

 L. 982        67  BREAK_LOOP       
               68  JUMP_FORWARD          2  'to 73'
               71  POP_TOP          
               72  END_FINALLY      
             73_0  COME_FROM            68  '68'
             73_1  COME_FROM            50  '50'

 L. 983        73  LOAD_GLOBAL           3  'len'
               76  LOAD_FAST             1  'text'
               79  CALL_FUNCTION_1       1  None
               82  STORE_FAST            6  'text_length'

 L. 990        85  LOAD_CONST               0
               88  STORE_FAST            7  'bracket_depth'

 L. 991        91  SETUP_LOOP          135  'to 229'
               94  LOAD_GLOBAL           4  'range'
               97  LOAD_FAST             5  'start_idx'
              100  LOAD_CONST               1
              103  BINARY_ADD       
              104  LOAD_GLOBAL           5  'min'
              107  LOAD_FAST             5  'start_idx'
              110  LOAD_FAST             2  'MAX_LINK_TEXT_SENTINEL'
              113  BINARY_ADD       

 L. 992       114  LOAD_FAST             6  'text_length'
              117  CALL_FUNCTION_2       2  None
              120  CALL_FUNCTION_2       2  None
              123  GET_ITER         
              124  FOR_ITER             88  'to 215'
              127  STORE_FAST            8  'p'

 L. 993       130  LOAD_FAST             1  'text'
              133  LOAD_FAST             8  'p'
              136  BINARY_SUBSCR    
              137  STORE_FAST            9  'ch'

 L. 994       140  LOAD_FAST             9  'ch'
              143  LOAD_CONST               ']'
              146  COMPARE_OP            2  ==
              149  JUMP_IF_FALSE        32  'to 184'
              152  POP_TOP          

 L. 995       153  LOAD_FAST             7  'bracket_depth'
              156  LOAD_CONST               1
              159  INPLACE_SUBTRACT 
              160  STORE_FAST            7  'bracket_depth'

 L. 996       163  LOAD_FAST             7  'bracket_depth'
              166  LOAD_CONST               0
              169  COMPARE_OP            0  <
              172  JUMP_IF_FALSE         5  'to 180'
              175  POP_TOP          

 L. 997       176  BREAK_LOOP       
              177  JUMP_ABSOLUTE       212  'to 212'
            180_0  COME_FROM           172  '172'
              180  POP_TOP          
              181  JUMP_BACK           124  'to 124'
            184_0  COME_FROM           149  '149'
              184  POP_TOP          

 L. 998       185  LOAD_FAST             9  'ch'
              188  LOAD_CONST               '['
              191  COMPARE_OP            2  ==
              194  JUMP_IF_FALSE        14  'to 211'
              197  POP_TOP          

 L. 999       198  LOAD_FAST             7  'bracket_depth'
              201  LOAD_CONST               1
              204  INPLACE_ADD      
              205  STORE_FAST            7  'bracket_depth'
              208  JUMP_BACK           124  'to 124'
            211_0  COME_FROM           194  '194'
              211  POP_TOP          
              212  JUMP_BACK           124  'to 124'
              215  POP_BLOCK        

 L.1003       216  LOAD_FAST             5  'start_idx'
              219  LOAD_CONST               1
              222  BINARY_ADD       
              223  STORE_FAST            4  'curr_pos'

 L.1004       226  JUMP_BACK            21  'to 21'
            229_0  COME_FROM            91  '91'

 L.1005       229  LOAD_FAST             1  'text'
              232  LOAD_FAST             5  'start_idx'
              235  LOAD_CONST               1
              238  BINARY_ADD       
              239  LOAD_FAST             8  'p'
              242  SLICE+3          
              243  STORE_FAST           10  'link_text'

 L.1008       246  LOAD_CONST               'footnotes'
              249  LOAD_FAST             0  'self'
              252  LOAD_ATTR             6  'extras'
              255  COMPARE_OP            6  in
              258  JUMP_IF_FALSE       148  'to 409'
              261  POP_TOP          
              262  LOAD_FAST            10  'link_text'
              265  LOAD_ATTR             7  'startswith'
              268  LOAD_CONST               '^'
              271  CALL_FUNCTION_1       1  None
            274_0  COME_FROM           258  '258'
              274  JUMP_IF_FALSE       132  'to 409'
            277_0  THEN                     410
              277  POP_TOP          

 L.1009       278  LOAD_GLOBAL           8  're'
              281  LOAD_ATTR             9  'sub'
              284  LOAD_CONST               '\\W'
              287  LOAD_CONST               '-'
              290  LOAD_FAST            10  'link_text'
              293  LOAD_CONST               1
              296  SLICE+1          
              297  CALL_FUNCTION_3       3  None
              300  STORE_FAST           11  'normed_id'

 L.1010       303  LOAD_FAST            11  'normed_id'
              306  LOAD_FAST             0  'self'
              309  LOAD_ATTR            10  'footnotes'
              312  COMPARE_OP            6  in
              315  JUMP_IF_FALSE        74  'to 392'
              318  POP_TOP          

 L.1011       319  LOAD_FAST             0  'self'
              322  LOAD_ATTR            11  'footnote_ids'
              325  LOAD_ATTR            12  'append'
              328  LOAD_FAST            11  'normed_id'
              331  CALL_FUNCTION_1       1  None
              334  POP_TOP          

 L.1012       335  LOAD_CONST               '<sup class="footnote-ref" id="fnref-%s"><a href="#fn-%s">%s</a></sup>'

 L.1014       338  LOAD_FAST            11  'normed_id'
              341  LOAD_FAST            11  'normed_id'
              344  LOAD_GLOBAL           3  'len'
              347  LOAD_FAST             0  'self'
              350  LOAD_ATTR            11  'footnote_ids'
              353  CALL_FUNCTION_1       1  None
              356  BUILD_TUPLE_3         3 
              359  BINARY_MODULO    
              360  STORE_FAST           12  'result'

 L.1015       363  LOAD_FAST             1  'text'
              366  LOAD_FAST             5  'start_idx'
              369  SLICE+2          
              370  LOAD_FAST            12  'result'
              373  BINARY_ADD       
              374  LOAD_FAST             1  'text'
              377  LOAD_FAST             8  'p'
              380  LOAD_CONST               1
              383  BINARY_ADD       
              384  SLICE+1          
              385  BINARY_ADD       
              386  STORE_FAST            1  'text'
              389  JUMP_BACK            21  'to 21'
            392_0  COME_FROM           315  '315'
              392  POP_TOP          

 L.1018       393  LOAD_FAST             8  'p'
              396  LOAD_CONST               1
              399  BINARY_ADD       
              400  STORE_FAST            4  'curr_pos'

 L.1019       403  CONTINUE             21  'to 21'
              406  JUMP_FORWARD          1  'to 410'
            409_0  COME_FROM           274  '274'
              409  POP_TOP          
            410_0  COME_FROM           406  '406'

 L.1022       410  LOAD_FAST             8  'p'
              413  LOAD_CONST               1
              416  INPLACE_ADD      
              417  STORE_FAST            8  'p'

 L.1023       420  LOAD_FAST             8  'p'
              423  LOAD_FAST             6  'text_length'
              426  COMPARE_OP            2  ==
              429  JUMP_IF_FALSE         5  'to 437'
            432_0  THEN                     437
              432  POP_TOP          

 L.1024       433  LOAD_FAST             1  'text'
              436  RETURN_END_IF    
              437  POP_TOP          

 L.1027       438  LOAD_FAST             1  'text'
              441  LOAD_FAST             8  'p'
              444  BINARY_SUBSCR    
              445  LOAD_CONST               '('
              448  COMPARE_OP            2  ==
              451  JUMP_IF_FALSE       468  'to 922'
              454  POP_TOP          

 L.1028       455  LOAD_FAST             0  'self'
              458  LOAD_ATTR            13  '_tail_of_inline_link_re'
              461  LOAD_ATTR            14  'match'
              464  LOAD_FAST             1  'text'
              467  LOAD_FAST             8  'p'
              470  CALL_FUNCTION_2       2  None
              473  STORE_FAST           13  'match'

 L.1029       476  LOAD_FAST            13  'match'
              479  JUMP_IF_FALSE       436  'to 918'
              482  POP_TOP          

 L.1031       483  LOAD_FAST             5  'start_idx'
              486  LOAD_CONST               0
              489  COMPARE_OP            4  >
              492  JUMP_IF_FALSE        18  'to 513'
              495  POP_TOP          
              496  LOAD_FAST             1  'text'
              499  LOAD_FAST             5  'start_idx'
              502  LOAD_CONST               1
              505  BINARY_SUBTRACT  
              506  BINARY_SUBSCR    
              507  LOAD_CONST               '!'
              510  COMPARE_OP            2  ==
            513_0  COME_FROM           492  '492'
              513  STORE_FAST           14  'is_img'

 L.1032       516  LOAD_FAST            14  'is_img'
              519  JUMP_IF_FALSE        14  'to 536'
            522_0  THEN                     537
              522  POP_TOP          

 L.1033       523  LOAD_FAST             5  'start_idx'
              526  LOAD_CONST               1
              529  INPLACE_SUBTRACT 
              530  STORE_FAST            5  'start_idx'
              533  JUMP_FORWARD          1  'to 537'
            536_0  COME_FROM           519  '519'
              536  POP_TOP          
            537_0  COME_FROM           533  '533'

 L.1035       537  LOAD_FAST            13  'match'
              540  LOAD_ATTR            15  'group'
              543  LOAD_CONST               'url'
              546  CALL_FUNCTION_1       1  None
              549  LOAD_FAST            13  'match'
              552  LOAD_ATTR            15  'group'
              555  LOAD_CONST               'title'
              558  CALL_FUNCTION_1       1  None
              561  ROT_TWO          
              562  STORE_FAST           15  'url'
              565  STORE_FAST           16  'title'

 L.1036       568  LOAD_FAST            15  'url'
              571  JUMP_IF_FALSE        34  'to 608'
              574  POP_TOP          
              575  LOAD_FAST            15  'url'
              578  LOAD_CONST               0
              581  BINARY_SUBSCR    
              582  LOAD_CONST               '<'
              585  COMPARE_OP            2  ==
            588_0  COME_FROM           571  '571'
              588  JUMP_IF_FALSE        17  'to 608'
            591_0  THEN                     609
              591  POP_TOP          

 L.1037       592  LOAD_FAST            15  'url'
              595  LOAD_CONST               1
              598  LOAD_CONST               -1
              601  SLICE+3          
              602  STORE_FAST           15  'url'
              605  JUMP_FORWARD          1  'to 609'
            608_0  COME_FROM           588  '588'
              608  POP_TOP          
            609_0  COME_FROM           605  '605'

 L.1040       609  LOAD_FAST             0  'self'
              612  LOAD_ATTR            16  '_process_url'
              615  LOAD_FAST            15  'url'
              618  CALL_FUNCTION_1       1  None
              621  STORE_FAST           15  'url'

 L.1041       624  LOAD_FAST            16  'title'
              627  JUMP_IF_FALSE        58  'to 688'
              630  POP_TOP          

 L.1042       631  LOAD_CONST               ' title="%s"'

 L.1043       634  LOAD_GLOBAL          17  '_xml_escape_attr'
              637  LOAD_FAST            16  'title'
              640  CALL_FUNCTION_1       1  None
              643  LOAD_ATTR            18  'replace'

 L.1044       646  LOAD_CONST               '*'
              649  LOAD_FAST             0  'self'
              652  LOAD_ATTR            19  '_escape_table'
              655  LOAD_CONST               '*'
              658  BINARY_SUBSCR    
              659  CALL_FUNCTION_2       2  None
              662  LOAD_ATTR            18  'replace'

 L.1045       665  LOAD_CONST               '_'
              668  LOAD_FAST             0  'self'
              671  LOAD_ATTR            19  '_escape_table'
              674  LOAD_CONST               '_'
              677  BINARY_SUBSCR    
              678  CALL_FUNCTION_2       2  None
              681  BINARY_MODULO    
              682  STORE_FAST           17  'title_str'
              685  JUMP_FORWARD          7  'to 695'
            688_0  COME_FROM           627  '627'
              688  POP_TOP          

 L.1047       689  LOAD_CONST               ''
              692  STORE_FAST           17  'title_str'
            695_0  COME_FROM           685  '685'

 L.1048       695  LOAD_FAST            14  'is_img'
              698  JUMP_IF_FALSE        91  'to 792'
              701  POP_TOP          

 L.1049       702  LOAD_CONST               '<img src="%s" alt="%s"%s%s'

 L.1050       705  LOAD_FAST            15  'url'
              708  LOAD_ATTR            18  'replace'
              711  LOAD_CONST               '"'
              714  LOAD_CONST               '&quot;'
              717  CALL_FUNCTION_2       2  None

 L.1051       720  LOAD_GLOBAL          17  '_xml_escape_attr'
              723  LOAD_FAST            10  'link_text'
              726  CALL_FUNCTION_1       1  None

 L.1052       729  LOAD_FAST            17  'title_str'
              732  LOAD_FAST             0  'self'
              735  LOAD_ATTR            20  'empty_element_suffix'
              738  BUILD_TUPLE_4         4 
              741  BINARY_MODULO    
              742  STORE_FAST           12  'result'

 L.1053       745  LOAD_FAST             5  'start_idx'
              748  LOAD_GLOBAL           3  'len'
              751  LOAD_FAST            12  'result'
              754  CALL_FUNCTION_1       1  None
              757  BINARY_ADD       
              758  STORE_FAST            4  'curr_pos'

 L.1054       761  LOAD_FAST             1  'text'
              764  LOAD_FAST             5  'start_idx'
              767  SLICE+2          
              768  LOAD_FAST            12  'result'
              771  BINARY_ADD       
              772  LOAD_FAST             1  'text'
              775  LOAD_FAST            13  'match'
              778  LOAD_ATTR            21  'end'
              781  CALL_FUNCTION_0       0  None
              784  SLICE+1          
              785  BINARY_ADD       
              786  STORE_FAST            1  'text'
              789  JUMP_BACK            21  'to 21'
            792_0  COME_FROM           698  '698'
              792  POP_TOP          

 L.1055       793  LOAD_FAST             5  'start_idx'
              796  LOAD_FAST             3  'anchor_allowed_pos'
              799  COMPARE_OP            5  >=
              802  JUMP_IF_FALSE        96  'to 901'
              805  POP_TOP          

 L.1056       806  LOAD_CONST               '<a href="%s"%s>'
              809  LOAD_FAST            15  'url'
              812  LOAD_FAST            17  'title_str'
              815  BUILD_TUPLE_2         2 
              818  BINARY_MODULO    
              819  STORE_FAST           18  'result_head'

 L.1057       822  LOAD_CONST               '%s%s</a>'
              825  LOAD_FAST            18  'result_head'
              828  LOAD_FAST            10  'link_text'
              831  BUILD_TUPLE_2         2 
              834  BINARY_MODULO    
              835  STORE_FAST           12  'result'

 L.1060       838  LOAD_FAST             5  'start_idx'
              841  LOAD_GLOBAL           3  'len'
              844  LOAD_FAST            18  'result_head'
              847  CALL_FUNCTION_1       1  None
              850  BINARY_ADD       
              851  STORE_FAST            4  'curr_pos'

 L.1061       854  LOAD_FAST             5  'start_idx'
              857  LOAD_GLOBAL           3  'len'
              860  LOAD_FAST            12  'result'
              863  CALL_FUNCTION_1       1  None
              866  BINARY_ADD       
              867  STORE_FAST            3  'anchor_allowed_pos'

 L.1062       870  LOAD_FAST             1  'text'
              873  LOAD_FAST             5  'start_idx'
              876  SLICE+2          
              877  LOAD_FAST            12  'result'
              880  BINARY_ADD       
              881  LOAD_FAST             1  'text'
              884  LOAD_FAST            13  'match'
              887  LOAD_ATTR            21  'end'
              890  CALL_FUNCTION_0       0  None
              893  SLICE+1          
              894  BINARY_ADD       
              895  STORE_FAST            1  'text'
              898  JUMP_BACK            21  'to 21'
            901_0  COME_FROM           802  '802'
              901  POP_TOP          

 L.1065       902  LOAD_FAST             5  'start_idx'
              905  LOAD_CONST               1
              908  BINARY_ADD       
              909  STORE_FAST            4  'curr_pos'

 L.1066       912  CONTINUE             21  'to 21'
              915  JUMP_ABSOLUTE      1434  'to 1434'
            918_0  COME_FROM           479  '479'
              918  POP_TOP          
              919  JUMP_FORWARD        512  'to 1434'
            922_0  COME_FROM           451  '451'
              922  POP_TOP          

 L.1070       923  LOAD_FAST             0  'self'
              926  LOAD_ATTR            22  '_tail_of_reference_link_re'
              929  LOAD_ATTR            14  'match'
              932  LOAD_FAST             1  'text'
              935  LOAD_FAST             8  'p'
              938  CALL_FUNCTION_2       2  None
              941  STORE_FAST           13  'match'

 L.1071       944  LOAD_FAST            13  'match'
              947  JUMP_IF_FALSE       483  'to 1433'
              950  POP_TOP          

 L.1073       951  LOAD_FAST             5  'start_idx'
              954  LOAD_CONST               0
              957  COMPARE_OP            4  >
              960  JUMP_IF_FALSE        18  'to 981'
              963  POP_TOP          
              964  LOAD_FAST             1  'text'
              967  LOAD_FAST             5  'start_idx'
              970  LOAD_CONST               1
              973  BINARY_SUBTRACT  
              974  BINARY_SUBSCR    
              975  LOAD_CONST               '!'
              978  COMPARE_OP            2  ==
            981_0  COME_FROM           960  '960'
              981  STORE_FAST           14  'is_img'

 L.1074       984  LOAD_FAST            14  'is_img'
              987  JUMP_IF_FALSE        14  'to 1004'
            990_0  THEN                     1005
              990  POP_TOP          

 L.1075       991  LOAD_FAST             5  'start_idx'
              994  LOAD_CONST               1
              997  INPLACE_SUBTRACT 
              998  STORE_FAST            5  'start_idx'
             1001  JUMP_FORWARD          1  'to 1005'
           1004_0  COME_FROM           987  '987'
             1004  POP_TOP          
           1005_0  COME_FROM          1001  '1001'

 L.1076      1005  LOAD_FAST            13  'match'
             1008  LOAD_ATTR            15  'group'
             1011  LOAD_CONST               'id'
             1014  CALL_FUNCTION_1       1  None
             1017  LOAD_ATTR            23  'lower'
             1020  CALL_FUNCTION_0       0  None
             1023  STORE_FAST           19  'link_id'

 L.1077      1026  LOAD_FAST            19  'link_id'
             1029  JUMP_IF_TRUE         16  'to 1048'
           1032_0  THEN                     1049
             1032  POP_TOP          

 L.1078      1033  LOAD_FAST            10  'link_text'
             1036  LOAD_ATTR            23  'lower'
             1039  CALL_FUNCTION_0       0  None
             1042  STORE_FAST           19  'link_id'
             1045  JUMP_FORWARD          1  'to 1049'
           1048_0  COME_FROM          1029  '1029'
             1048  POP_TOP          
           1049_0  COME_FROM          1045  '1045'

 L.1079      1049  LOAD_FAST            19  'link_id'
             1052  LOAD_FAST             0  'self'
             1055  LOAD_ATTR            24  'urls'
             1058  COMPARE_OP            6  in
             1061  JUMP_IF_FALSE       350  'to 1414'
             1064  POP_TOP          

 L.1080      1065  LOAD_FAST             0  'self'
             1068  LOAD_ATTR            16  '_process_url'
             1071  LOAD_FAST             0  'self'
             1074  LOAD_ATTR            24  'urls'
             1077  LOAD_FAST            19  'link_id'
             1080  BINARY_SUBSCR    
             1081  CALL_FUNCTION_1       1  None
             1084  STORE_FAST           15  'url'

 L.1081      1087  LOAD_FAST             0  'self'
             1090  LOAD_ATTR            25  'titles'
             1093  LOAD_ATTR            26  'get'
             1096  LOAD_FAST            19  'link_id'
             1099  CALL_FUNCTION_1       1  None
             1102  STORE_FAST           16  'title'

 L.1082      1105  LOAD_FAST            16  'title'
             1108  JUMP_IF_FALSE        70  'to 1181'
             1111  POP_TOP          

 L.1083      1112  LOAD_FAST            16  'title'
             1115  STORE_FAST           20  'before'

 L.1084      1118  LOAD_GLOBAL          17  '_xml_escape_attr'
             1121  LOAD_FAST            16  'title'
             1124  CALL_FUNCTION_1       1  None
             1127  LOAD_ATTR            18  'replace'

 L.1085      1130  LOAD_CONST               '*'
             1133  LOAD_FAST             0  'self'
             1136  LOAD_ATTR            19  '_escape_table'
             1139  LOAD_CONST               '*'
             1142  BINARY_SUBSCR    
             1143  CALL_FUNCTION_2       2  None
             1146  LOAD_ATTR            18  'replace'

 L.1086      1149  LOAD_CONST               '_'
             1152  LOAD_FAST             0  'self'
             1155  LOAD_ATTR            19  '_escape_table'
             1158  LOAD_CONST               '_'
             1161  BINARY_SUBSCR    
             1162  CALL_FUNCTION_2       2  None
             1165  STORE_FAST           16  'title'

 L.1087      1168  LOAD_CONST               ' title="%s"'
             1171  LOAD_FAST            16  'title'
             1174  BINARY_MODULO    
             1175  STORE_FAST           17  'title_str'
             1178  JUMP_FORWARD          7  'to 1188'
           1181_0  COME_FROM          1108  '1108'
             1181  POP_TOP          

 L.1089      1182  LOAD_CONST               ''
             1185  STORE_FAST           17  'title_str'
           1188_0  COME_FROM          1178  '1178'

 L.1090      1188  LOAD_FAST            14  'is_img'
             1191  JUMP_IF_FALSE        97  'to 1291'
             1194  POP_TOP          

 L.1091      1195  LOAD_CONST               '<img src="%s" alt="%s"%s%s'

 L.1092      1198  LOAD_FAST            15  'url'
             1201  LOAD_ATTR            18  'replace'
             1204  LOAD_CONST               '"'
             1207  LOAD_CONST               '&quot;'
             1210  CALL_FUNCTION_2       2  None

 L.1093      1213  LOAD_FAST            10  'link_text'
             1216  LOAD_ATTR            18  'replace'
             1219  LOAD_CONST               '"'
             1222  LOAD_CONST               '&quot;'
             1225  CALL_FUNCTION_2       2  None

 L.1094      1228  LOAD_FAST            17  'title_str'
             1231  LOAD_FAST             0  'self'
             1234  LOAD_ATTR            20  'empty_element_suffix'
             1237  BUILD_TUPLE_4         4 
             1240  BINARY_MODULO    
             1241  STORE_FAST           12  'result'

 L.1095      1244  LOAD_FAST             5  'start_idx'
             1247  LOAD_GLOBAL           3  'len'
             1250  LOAD_FAST            12  'result'
             1253  CALL_FUNCTION_1       1  None
             1256  BINARY_ADD       
             1257  STORE_FAST            4  'curr_pos'

 L.1096      1260  LOAD_FAST             1  'text'
             1263  LOAD_FAST             5  'start_idx'
             1266  SLICE+2          
             1267  LOAD_FAST            12  'result'
             1270  BINARY_ADD       
             1271  LOAD_FAST             1  'text'
             1274  LOAD_FAST            13  'match'
             1277  LOAD_ATTR            21  'end'
             1280  CALL_FUNCTION_0       0  None
             1283  SLICE+1          
             1284  BINARY_ADD       
             1285  STORE_FAST            1  'text'
             1288  JUMP_ABSOLUTE      1427  'to 1427'
           1291_0  COME_FROM          1191  '1191'
             1291  POP_TOP          

 L.1097      1292  LOAD_FAST             5  'start_idx'
             1295  LOAD_FAST             3  'anchor_allowed_pos'
             1298  COMPARE_OP            5  >=
             1301  JUMP_IF_FALSE        96  'to 1400'
             1304  POP_TOP          

 L.1098      1305  LOAD_CONST               '<a href="%s"%s>'
             1308  LOAD_FAST            15  'url'
             1311  LOAD_FAST            17  'title_str'
             1314  BUILD_TUPLE_2         2 
             1317  BINARY_MODULO    
             1318  STORE_FAST           18  'result_head'

 L.1099      1321  LOAD_CONST               '%s%s</a>'
             1324  LOAD_FAST            18  'result_head'
             1327  LOAD_FAST            10  'link_text'
             1330  BUILD_TUPLE_2         2 
             1333  BINARY_MODULO    
             1334  STORE_FAST           12  'result'

 L.1102      1337  LOAD_FAST             5  'start_idx'
             1340  LOAD_GLOBAL           3  'len'
             1343  LOAD_FAST            18  'result_head'
             1346  CALL_FUNCTION_1       1  None
             1349  BINARY_ADD       
             1350  STORE_FAST            4  'curr_pos'

 L.1103      1353  LOAD_FAST             5  'start_idx'
             1356  LOAD_GLOBAL           3  'len'
             1359  LOAD_FAST            12  'result'
             1362  CALL_FUNCTION_1       1  None
             1365  BINARY_ADD       
             1366  STORE_FAST            3  'anchor_allowed_pos'

 L.1104      1369  LOAD_FAST             1  'text'
             1372  LOAD_FAST             5  'start_idx'
             1375  SLICE+2          
             1376  LOAD_FAST            12  'result'
             1379  BINARY_ADD       
             1380  LOAD_FAST             1  'text'
             1383  LOAD_FAST            13  'match'
             1386  LOAD_ATTR            21  'end'
             1389  CALL_FUNCTION_0       0  None
             1392  SLICE+1          
             1393  BINARY_ADD       
             1394  STORE_FAST            1  'text'
             1397  JUMP_ABSOLUTE      1427  'to 1427'
           1400_0  COME_FROM          1301  '1301'
             1400  POP_TOP          

 L.1107      1401  LOAD_FAST             5  'start_idx'
             1404  LOAD_CONST               1
             1407  BINARY_ADD       
             1408  STORE_FAST            4  'curr_pos'
             1411  JUMP_BACK            21  'to 21'
           1414_0  COME_FROM          1061  '1061'
             1414  POP_TOP          

 L.1110      1415  LOAD_FAST            13  'match'
             1418  LOAD_ATTR            21  'end'
             1421  CALL_FUNCTION_0       0  None
             1424  STORE_FAST            4  'curr_pos'

 L.1111      1427  CONTINUE             21  'to 21'
             1430  JUMP_FORWARD          1  'to 1434'
           1433_0  COME_FROM           947  '947'
             1433  POP_TOP          
           1434_0  COME_FROM          1430  '1430'
           1434_1  COME_FROM           919  '919'

 L.1114      1434  LOAD_FAST             5  'start_idx'
             1437  LOAD_CONST               1
             1440  BINARY_ADD       
             1441  STORE_FAST            4  'curr_pos'
             1444  JUMP_BACK            21  'to 21'
             1447  POP_TOP          
             1448  POP_BLOCK        
           1449_0  COME_FROM            18  '18'

 L.1116      1449  LOAD_FAST             1  'text'
             1452  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 229

    def _process_url(self, url):
        return to_url(url.replace('*', self._escape_table['*']).replace('_', self._escape_table['_']), force=True)

    def header_id_from_text(self, text, prefix, n):
        """Generate a header id attribute value from the given header
        HTML content.
        
        This is only called if the "header-ids" extra is enabled.
        Subclasses may override this for different header ids.
        
        @param text {str} The text of the header tag
        @param prefix {str} The requested prefix for header ids. This is the
            value of the "header-ids" extra key, if any. Otherwise, None.
        @param n {int} The <hN> tag number, i.e. `1` for an <h1> tag.
        @returns {str} The value for the header tag's "id" attribute. Return
            None to not have an id attribute and to exclude this header from
            the TOC (if the "toc" extra is specified).
        """
        header_id = _slugify(text)
        if prefix and isinstance(prefix, basestring):
            header_id = prefix + '-' + header_id
        if header_id in self._count_from_header_id:
            self._count_from_header_id[header_id] += 1
            header_id += '-%s' % self._count_from_header_id[header_id]
        else:
            self._count_from_header_id[header_id] = 1
        return header_id

    _toc = None

    def _toc_add_entry(self, level, id, name):
        if self._toc is None:
            self._toc = []
        self._toc.append((level, id, name))
        return

    _setext_h_re = re.compile('^(.+)[ \\t]*\\n(=+|-+)[ \\t]*\\n+', re.M)

    def _setext_h_sub(self, match):
        n = {'=': 1, '-': 2}[match.group(2)[0]]
        demote_headers = self.extras.get('demote-headers')
        if demote_headers:
            n = min(n + demote_headers, 6)
        header_id_attr = ''
        if 'header-ids' in self.extras:
            header_id = self.header_id_from_text(match.group(1), self.extras['header-ids'], n)
            if header_id:
                header_id_attr = ' id="%s"' % header_id
        html = self._run_span_gamut(match.group(1))
        if 'toc' in self.extras and header_id:
            self._toc_add_entry(n, header_id, html)
        return '<h%d%s>%s</h%d>\n\n' % (n, header_id_attr, html, n)

    _atx_h_re = re.compile("\n        ^(\\#{1,6})  # \\1 = string of #'s\n        [ \\t]*\n        (.+?)       # \\2 = Header text\n        [ \\t]*\n        (?<!\\\\)     # ensure not an escaped trailing '#'\n        \\#*         # optional closing #'s (not counted)\n        \\n+\n        ", re.X | re.M)

    def _atx_h_sub(self, match):
        n = len(match.group(1))
        demote_headers = self.extras.get('demote-headers')
        if demote_headers:
            n = min(n + demote_headers, 6)
        header_id_attr = ''
        if 'header-ids' in self.extras:
            header_id = self.header_id_from_text(match.group(2), self.extras['header-ids'], n)
            if header_id:
                header_id_attr = ' id="%s"' % header_id
        html = self._run_span_gamut(match.group(2))
        if 'toc' in self.extras and header_id:
            self._toc_add_entry(n, header_id, html)
        return '<h%d%s>%s</h%d>\n\n' % (n, header_id_attr, html, n)

    def _do_headers(self, text):
        text = self._setext_h_re.sub(self._setext_h_sub, text)
        text = self._atx_h_re.sub(self._atx_h_sub, text)
        return text

    _marker_ul_chars = '*+-'
    _marker_any = '(?:[%s]|\\d+\\.)' % _marker_ul_chars
    _marker_ul = '(?:[%s])' % _marker_ul_chars
    _marker_ol = '(?:\\d+\\.)'

    def _list_sub(self, match):
        lst = match.group(1)
        lst_type = match.group(3) in self._marker_ul_chars and 'ul' or 'ol'
        result = self._process_list_items(lst)
        if self.list_level:
            return '<%s>\n%s</%s>\n' % (lst_type, result, lst_type)
        else:
            return '<%s>\n%s</%s>\n\n' % (lst_type, result, lst_type)

    def _do_lists(self, text):
        for marker_pat in (self._marker_ul, self._marker_ol):
            less_than_tab = self.tab_width - 1
            whole_list = "\n                (                   # \\1 = whole list\n                  (                 # \\2\n                    [ ]{0,%d}\n                    (%s)            # \\3 = first list item marker\n                    [ \\t]+\n                    (?!\\ *\\3\\ )     # '- - - ...' isn't a list. See 'not_quite_a_list' test case.\n                  )\n                  (?:.+?)\n                  (                 # \\4\n                      \\Z\n                    |\n                      \\n{2,}\n                      (?=\\S)\n                      (?!           # Negative lookahead for another list item marker\n                        [ \\t]*\n                        %s[ \\t]+\n                      )\n                  )\n                )\n            " % (less_than_tab, marker_pat, marker_pat)
            if self.list_level:
                sub_list_re = re.compile('^' + whole_list, re.X | re.M | re.S)
                text = sub_list_re.sub(self._list_sub, text)
            else:
                list_re = re.compile('(?:(?<=\\n\\n)|\\A\\n?)' + whole_list, re.X | re.M | re.S)
                text = list_re.sub(self._list_sub, text)

        return text

    _list_item_re = re.compile('\n        (\\n)?                   # leading line = \\1\n        (^[ \\t]*)               # leading whitespace = \\2\n        (?P<marker>%s) [ \\t]+   # list marker = \\3\n        ((?:.+?)                # list item text = \\4\n         (\\n{1,2}))             # eols = \\5\n        (?= \\n* (\\Z | \\2 (?P<next_marker>%s) [ \\t]+))\n        ' % (_marker_any, _marker_any), re.M | re.X | re.S)
    _last_li_endswith_two_eols = False

    def _list_item_sub(self, match):
        item = match.group(4)
        leading_line = match.group(1)
        leading_space = match.group(2)
        if leading_line or '\n\n' in item or self._last_li_endswith_two_eols:
            item = self._run_block_gamut(self._outdent(item))
        else:
            item = self._do_lists(self._outdent(item))
            if item.endswith('\n'):
                item = item[:-1]
            item = self._run_span_gamut(item)
        self._last_li_endswith_two_eols = len(match.group(5)) == 2
        return '<li>%s</li>\n' % item

    def _process_list_items(self, list_str):
        self.list_level += 1
        self._last_li_endswith_two_eols = False
        list_str = list_str.rstrip('\n') + '\n'
        list_str = self._list_item_re.sub(self._list_item_sub, list_str)
        self.list_level -= 1
        return list_str

    def _get_pygments_lexer(self, lexer_name):
        try:
            from pygments import lexers, util
        except ImportError:
            return
        else:
            try:
                return lexers.get_lexer_by_name(lexer_name)
            except util.ClassNotFound:
                return

        return

    def _color_with_pygments(self, codeblock, lexer, **formatter_opts):
        import pygments, pygments.formatters

        class HtmlCodeFormatter(pygments.formatters.HtmlFormatter):

            def _wrap_code(self, inner):
                """A function for use in a Pygments Formatter which
                wraps in <code> tags.
                """
                yield (0, '<code>')
                for tup in inner:
                    yield tup

                yield (0, '</code>')

            def wrap(self, source, outfile):
                """Return the source with a code, pre, and div."""
                return self._wrap_div(self._wrap_pre(self._wrap_code(source)))

        formatter = HtmlCodeFormatter(cssclass='codehilite', **formatter_opts)
        return pygments.highlight(codeblock, lexer, formatter)

    def _code_block_sub(self, match):
        codeblock = match.group(1)
        codeblock = self._outdent(codeblock)
        codeblock = self._detab(codeblock)
        codeblock = codeblock.lstrip('\n')
        codeblock = codeblock.rstrip()
        if 'code-color' in self.extras and codeblock.startswith(':::'):
            (lexer_name, rest) = codeblock.split('\n', 1)
            lexer_name = lexer_name[3:].strip()
            lexer = self._get_pygments_lexer(lexer_name)
            codeblock = rest.lstrip('\n')
            if lexer:
                formatter_opts = self.extras['code-color'] or {}
                colored = self._color_with_pygments(codeblock, lexer, **formatter_opts)
                return '\n\n%s\n\n' % colored
        codeblock = self._encode_code(codeblock)
        pre_class_str = self._html_class_str_from_tag('pre')
        code_class_str = self._html_class_str_from_tag('code')
        return '\n\n<pre%s><code%s>%s\n</code></pre>\n\n' % (
         pre_class_str, code_class_str, codeblock)

    def _html_class_str_from_tag(self, tag):
        """Get the appropriate ' class="..."' string (note the leading
        space), if any, for the given tag.
        """
        if 'html-classes' not in self.extras:
            return ''
        try:
            html_classes_from_tag = self.extras['html-classes']
        except TypeError:
            return ''

        if tag in html_classes_from_tag:
            return ' class="%s"' % html_classes_from_tag[tag]
        return ''

    def _do_code_blocks(self, text):
        """Process Markdown `<pre><code>` blocks."""
        code_block_re = re.compile('\n            (?:\\n\\n|\\A)\n            (               # $1 = the code block -- one or more lines, starting with a space/tab\n              (?:\n                (?:[ ]{%d} | \\t)  # Lines must start with a tab or a tab-width of spaces\n                .*\\n+\n              )+\n            )\n            ((?=^[ ]{0,%d}\\S)|\\Z)   # Lookahead for non-space at line-start, or end of doc\n            ' % (self.tab_width, self.tab_width), re.M | re.X)
        return code_block_re.sub(self._code_block_sub, text)

    _code_span_re = re.compile('\n            (?<!\\\\)\n            (`+)        # \\1 = Opening run of `\n            (?!`)       # See Note A test/tm-cases/escapes.text\n            (.+?)       # \\2 = The code block\n            (?<!`)\n            \\1          # Matching closer\n            (?!`)\n        ', re.X | re.S)

    def _code_span_sub(self, match):
        c = match.group(2).strip(' \t')
        c = self._encode_code(c)
        return '<code>%s</code>' % c

    def _do_code_spans(self, text):
        return self._code_span_re.sub(self._code_span_sub, text)

    def _encode_code(self, text):
        """Encode/escape certain characters inside Markdown code runs.
        The point is that in code, these characters are literals,
        and lose their special Markdown meanings.
        """
        replacements = [
         ('&', '&amp;'),
         ('<', '&lt;'),
         ('>', '&gt;'),
         (
          '*', self._escape_table['*']),
         (
          '_', self._escape_table['_']),
         (
          '{', self._escape_table['{']),
         (
          '}', self._escape_table['}']),
         (
          '[', self._escape_table['[']),
         (
          ']', self._escape_table[']']),
         (
          '\\', self._escape_table['\\'])]
        for (before, after) in replacements:
            text = text.replace(before, after)

        return text

    _strong_re = re.compile('\n                               (\n                                 \\*\\*\n                                  | __\n                               )\n                               (?=\n                                 \\S\n                               )\n                               (\n                                 . +?\n                                 [*_] *\n                               )\n                               (?<=\n                                 \\S\n                               )\n                               \\1\n                              ', re.S | re.X)
    _em_re = re.compile('\n                           (\n                             \\*\n                              | _ \n                           )\n                           (?=\n                             \\S\n                           )\n                           (\n                             . +?\n                           )\n                           (?<=\n                             \\S\n                           )\n                           \\1\n                          ', re.S | re.X)
    _code_friendly_strong_re = re.compile('\n                                             \\*\\*\n                                             (?=\n                                               \\S\n                                             )\n                                             (\n                                               . +?\n                                               [*_]*\n                                             )\n                                             (?<=\n                                               \\S\n                                             )\n                                             \\*\\*\n                                            ', re.S | re.X)
    _code_friendly_em_re = re.compile('\n                                         \\*\n                                         (?=\n                                           \\S\n                                         )\n                                         (\n                                           . +?\n                                         )\n                                         (?<=\n                                           \\S\n                                         )\n                                         \\*\n                                        ', re.S | re.X)

    def _do_italics_and_bold(self, text):
        if 'code-friendly' in self.extras:
            text = self._code_friendly_strong_re.sub('<strong>\\1</strong>', text)
            text = self._code_friendly_em_re.sub('<em>\\1</em>', text)
        else:
            text = self._strong_re.sub('<strong>\\2</strong>', text)
            text = self._em_re.sub('<em>\\2</em>', text)
        return text

    _apostrophe_year_re = re.compile("'(\\d\\d)(?=(\\s|,|;|\\.|\\?|!|$))")
    _contractions = ['tis', 'twas', 'twer', 'neath', 'o', 'n',
     'round', 'bout', 'twixt', 'nuff', 'fraid', 'sup']

    def _do_smart_contractions(self, text):
        text = self._apostrophe_year_re.sub('&#8217;\\1', text)
        for c in self._contractions:
            text = text.replace("'%s" % c, '&#8217;%s' % c)
            text = text.replace("'%s" % c.capitalize(), '&#8217;%s' % c.capitalize())

        return text

    _opening_single_quote_re = re.compile("\n                                             (?<!\n                                               \\S\n                                             )\n                                             '\n                                             (?=\n                                               \\S\n                                             )\n                                            ", re.X)
    _opening_double_quote_re = re.compile('\n                                             (?<!\n                                               \\S\n                                             )\n                                             "\n                                             (?=\n                                               \\S\n                                             )\n                                            ', re.X)
    _closing_single_quote_re = re.compile("\n                                             (?<=\n                                               \\S\n                                             )\n                                             '\n                                            ", re.X)
    _closing_double_quote_re = re.compile('\n                                             (?<=\n                                               \\S\n                                             )\n                                             "\n                                             (?=\n                                               (\n                                                 \\s\n                                                  | ,\n                                                  | ;\n                                                  | \\.\n                                                  | \\?\n                                                  | !\n                                                  | $\n                                                )\n                                              )\n                                             ', re.X)

    def _do_smart_punctuation(self, text):
        """Fancifies 'single quotes', "double quotes", and apostrophes.  
        Converts --, ---, and ... into en dashes, em dashes, and ellipses.
        
        Inspiration is: <http://daringfireball.net/projects/smartypants/>
        See "test/tm-cases/smarty_pants.text" for a full discussion of the
        support here and
        <http://code.google.com/p/python-markdown2/issues/detail?id=42> for a
        discussion of some diversion from the original SmartyPants.
        """
        text = text.replace('---', '&#8212;')
        text = text.replace('--', '&#8211;')
        text = text.replace('...', '&#8230;')
        text = text.replace(' . . . ', '&#8230;')
        text = text.replace('. . .', '&#8230;')
        return text

    _block_quote_re = re.compile("\n        (                           # Wrap whole match in \\1\n          (\n            ^[ \\t]*>[ \\t]?          # '>' at the start of a line\n              .+\\n                  # rest of the first line\n            (.+\\n)*                 # subsequent consecutive lines\n            \\n*                     # blanks\n          )+\n        )\n        ", re.M | re.X)
    _bq_one_level_re = re.compile('^[ \t]*>[ \t]?', re.M)
    _html_pre_block_re = re.compile('(\\s*<pre>.+?</pre>)', re.S)

    def _dedent_two_spaces_sub(self, match):
        return re.sub('(?m)^  ', '', match.group(1))

    def _block_quote_sub(self, match):
        bq = match.group(1)
        bq = self._bq_one_level_re.sub('', bq)
        bq = _blank_line_re.sub('', bq)
        bq = self._run_block_gamut(bq)
        bq = re.sub('(?m)^', '  ', bq)
        bq = self._html_pre_block_re.sub(self._dedent_two_spaces_sub, bq)
        return '<blockquote>\n%s\n</blockquote>\n\n' % bq

    def _do_block_quotes(self, text):
        if '>' not in text:
            return text
        return self._block_quote_re.sub(self._block_quote_sub, text)

    def _form_paragraphs(self, text):
        text = text.strip('\n')
        grafs = []
        for graf in re.split('\\n{2,}', text):
            if graf in self.html_blocks:
                grafs.append(self.html_blocks[graf])
            else:
                cuddled_list = None
                if 'cuddled-lists' in self.extras:
                    li = self._list_item_re.search(graf + '\n')
                    if li and len(li.group(2)) <= 3 and li.group('next_marker'):
                        if li.group('marker')[(-1)] == li.group('next_marker')[(-1)]:
                            start = li.start()
                            cuddled_list = self._do_lists(graf[start:]).rstrip('\n')
                            assert cuddled_list.startswith('<ul>') or cuddled_list.startswith('<ol>')
                            graf = graf[:start]
                    graf = self._run_span_gamut(graf).lstrip(' \t')
                    grafs.append(tags.HTML.p(literal(graf), class_=self.p_class) if not self.inline else graf)
                elif cuddled_list:
                    grafs.append(cuddled_list)

        return ('\n\n').join(grafs)

    def _add_footnotes(self, text):
        if self.footnotes:
            footer = ['<div class="footnotes">',
             '<hr' + self.empty_element_suffix,
             '<ol>']
            for (i, id) in enumerate(self.footnote_ids):
                if i != 0:
                    footer.append('')
                footer.append('<li id="fn-%s">' % id)
                footer.append(self._run_block_gamut(self.footnotes[id]))
                backlink = '<a href="#fnref-%s" class="footnoteBackLink" title="Jump back to footnote %d in the text.">&#8617;</a>' % (
                 id, i + 1)
                if footer[(-1)].endswith('</p>'):
                    footer[-1] = footer[(-1)][:-len('</p>')] + '&nbsp;' + backlink + '</p>'
                else:
                    footer.append('\n<p>%s</p>' % backlink)
                footer.append('</li>')

            footer.append('</ol>')
            footer.append('</div>')
            return text + '\n\n' + ('\n').join(footer)
        else:
            return text

    _ampersand_re = re.compile('\n                                  &\n                                  (?!\n                                    \\# ?\n                                    [xX] ?\n                                    \\w +\n                                    ;\n                                  )\n                                 ', re.X)
    _naked_lt_re = re.compile('\n                                 <\n                                 (?!\n                                   [a-z/?\\$!]\n                                 )\n                                ', re.I | re.X)
    _naked_gt_re = re.compile('\n                                 (?<!\n                                   [a-z?!/\'"-]\n                                 )\n                                 >\n                                ', re.I | re.X)

    def _encode_amps_and_angles(self, text):
        text = self._ampersand_re.sub('&amp;', text)
        text = self._naked_lt_re.sub('&lt;', text)
        text = self._naked_gt_re.sub('&gt;', text)
        return text

    def _encode_backslash_escapes(self, text):
        for (ch, escape) in self._escape_table.items():
            text = text.replace('\\' + ch, escape)

        return text

    def _encode_email_address(self, addr):
        chars = [ _xml_encode_email_char_at_random(ch) for ch in 'mailto:' + addr
                ]
        addr = '<a href="%s">%s</a>' % (
         ('').join(chars), ('').join(chars[7:]))
        return addr

    def _do_link_patterns(self, text):
        """Caveat emptor: there isn't much guarding against link
        patterns being formed inside other standard Markdown links, e.g.
        inside a [link def][like this].

        Dev Notes: *Could* consider prefixing regexes with a negative
        lookbehind assertion to attempt to guard against this.
        """
        link_from_hash = {}
        for tup in self.link_patterns:
            if len(tup) == 2:
                (regex, repl) = tup
                do_link = True
            else:
                (regex, repl, do_link) = tup
            replacements = []
            for match in regex.finditer(text):
                if hasattr(repl, '__call__'):
                    href = repl(match)
                else:
                    href = match.expand(repl)
                replacements.append((match.span(), href))

            for ((start, end), href) in reversed(replacements):
                escaped_href = href.replace('"', '&quot;').replace('*', self._escape_table['*']).replace('_', self._escape_table['_'])
                if do_link:
                    link = '<a class="linkPattern" href="%s">%s</a>' % (escaped_href, text[start:end])
                else:
                    link = href
                hash = _hash_text(link)
                link_from_hash[hash] = link
                text = text[:start] + hash + text[end:]

        for (hash, link) in link_from_hash.items():
            text = text.replace(hash, link)

        return text

    def _unescape_special_chars(self, text):
        for (ch, hash) in self._escape_table.items():
            text = text.replace(hash, ch)

        return text

    def _outdent(self, text):
        return self._outdent_re.sub('', text)


class MarkdownWithExtras(Markdown):
    """A markdowner class that enables most extras:

    - footnotes
    - code-color (only has effect if 'pygments' Python module on path)

    These are not included:
    - pyshell (specific to Python-related documenting)
    - code-friendly (because it *disables* part of the syntax)
    - link-patterns (because you need to specify some actual
      link-patterns anyway)
    """
    extras = [
     'footnotes', 'code-color']


class UnicodeWithAttrs(unicode):
    """A subclass of unicode used for the return value of conversion to
    possibly attach some attributes. E.g. the "toc_html" attribute when
    the "toc" extra is used.
    """
    _toc = None

    @property
    def toc_html(self):
        """Return the HTML for the current TOC.
        
        This expects the `_toc` attribute to have been set on this instance.
        """
        if self._toc is None:
            return
        else:

            def indent():
                return '  ' * (len(h_stack) - 1)

            lines = []
            h_stack = [0]
            for (level, id, name) in self._toc:
                if level > h_stack[(-1)]:
                    lines.append('%s<ul>' % indent())
                    h_stack.append(level)
                elif level == h_stack[(-1)]:
                    lines[(-1)] += '</li>'
                else:
                    while level < h_stack[(-1)]:
                        h_stack.pop()
                        if not lines[(-1)].endswith('</li>'):
                            lines[(-1)] += '</li>'
                        lines.append('%s</ul></li>' % indent())

                    lines.append('%s<li><a href="#%s">%s</a>' % (
                     indent(), id, name))

            while len(h_stack) > 1:
                h_stack.pop()
                if not lines[(-1)].endswith('</li>'):
                    lines[(-1)] += '</li>'
                lines.append('%s</ul>' % indent())

            return ('\n').join(lines) + '\n'


_slugify_strip_re = re.compile('[^\\w\\s-]')
_slugify_hyphenate_re = re.compile('[-\\s]+')

def _slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    
    From Django's "django/template/defaultfilters.py".
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(_slugify_strip_re.sub('', value).strip().lower())
    return _slugify_hyphenate_re.sub('-', value)


def _curry(*args, **kwargs):
    function, args = args[0], args[1:]

    def result(*rest, **kwrest):
        combined = kwargs.copy()
        combined.update(kwrest)
        return function(*(args + rest), **combined)

    return result


def _regex_from_encoded_pattern(s):
    """'foo'    -> re.compile(re.escape('foo'))
       '/foo/'  -> re.compile('foo')
       '/foo/i' -> re.compile('foo', re.I)
    """
    if s.startswith('/') and s.rfind('/') != 0:
        idx = s.rfind('/')
        pattern, flags_str = s[1:idx], s[idx + 1:]
        flag_from_char = {'i': re.IGNORECASE, 
           'l': re.LOCALE, 
           's': re.DOTALL, 
           'm': re.MULTILINE, 
           'u': re.UNICODE}
        flags = 0
        for char in flags_str:
            try:
                flags |= flag_from_char[char]
            except KeyError:
                raise ValueError("unsupported regex flag: '%s' in '%s' (must be one of '%s')" % (
                 char, s, ('').join(flag_from_char.keys())))

        return re.compile(s[1:idx], flags)
    else:
        return re.compile(re.escape(s))


def _dedentlines(lines, tabsize=8, skip_first_line=False):
    """_dedentlines(lines, tabsize=8, skip_first_line=False) -> dedented lines
    
        "lines" is a list of lines to dedent.
        "tabsize" is the tab width to use for indent width calculations.
        "skip_first_line" is a boolean indicating if the first line should
            be skipped for calculating the indent width and for dedenting.
            This is sometimes useful for docstrings and similar.
    
    Same as dedent() except operates on a sequence of lines. Note: the
    lines list is modified **in-place**.
    """
    DEBUG = False
    if DEBUG:
        print 'dedent: dedent(..., tabsize=%d, skip_first_line=%r)' % (
         tabsize, skip_first_line)
    indents = []
    margin = None
    for (i, line) in enumerate(lines):
        if i == 0 and skip_first_line:
            continue
        indent = 0
        for ch in line:
            if ch == ' ':
                indent += 1
            elif ch == '\t':
                indent += tabsize - indent % tabsize
            elif ch in '\r\n':
                continue
            else:
                break
        else:
            continue

        if DEBUG:
            print 'dedent: indent=%d: %r' % (indent, line)
        if margin is None:
            margin = indent
        else:
            margin = min(margin, indent)

    if DEBUG:
        print 'dedent: margin=%r' % margin
    if margin is not None and margin > 0:
        for (i, line) in enumerate(lines):
            if i == 0 and skip_first_line:
                continue
            removed = 0
            for (j, ch) in enumerate(line):
                if ch == ' ':
                    removed += 1
                elif ch == '\t':
                    removed += tabsize - removed % tabsize
                elif ch in '\r\n':
                    if DEBUG:
                        print 'dedent: %r: EOL -> strip up to EOL' % line
                    lines[i] = lines[i][j:]
                    break
                else:
                    raise ValueError('unexpected non-whitespace char %r in line %r while removing %d-space margin' % (
                     ch, line, margin))
                if DEBUG:
                    print 'dedent: %r: %r -> removed %d/%d' % (
                     line, ch, removed, margin)
                if removed == margin:
                    lines[i] = lines[i][j + 1:]
                    break
                elif removed > margin:
                    lines[i] = ' ' * (removed - margin) + lines[i][j + 1:]
                    break
            else:
                if removed:
                    lines[i] = lines[i][removed:]

    return lines


def _dedent(text, tabsize=8, skip_first_line=False):
    """_dedent(text, tabsize=8, skip_first_line=False) -> dedented text

        "text" is the text to dedent.
        "tabsize" is the tab width to use for indent width calculations.
        "skip_first_line" is a boolean indicating if the first line should
            be skipped for calculating the indent width and for dedenting.
            This is sometimes useful for docstrings and similar.
    
    textwrap.dedent(s), but don't expand tabs to spaces
    """
    lines = text.splitlines(1)
    _dedentlines(lines, tabsize=tabsize, skip_first_line=skip_first_line)
    return ('').join(lines)


class _memoized(object):
    """Decorator that caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned, and
   not re-evaluated.

   http://wiki.python.org/moin/PythonDecoratorLibrary
   """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            self.cache[args] = value = self.func(*args)
            return value
        except TypeError:
            return self.func(*args)

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__


def _xml_oneliner_re_from_tab_width(tab_width):
    """Standalone XML processing instruction regex."""
    return re.compile('\n        (?:\n            (?<=\\n\\n)       # Starting after a blank line\n            |               # or\n            \\A\\n?           # the beginning of the doc\n        )\n        (                           # save in $1\n            [ ]{0,%d}\n            (?:\n                <\\?\\w+\\b\\s+.*?\\?>   # XML processing instruction\n                |\n                <\\w+:\\w+\\b\\s+.*?/>  # namespaced single tag\n            )\n            [ \\t]*\n            (?=\\n{2,}|\\Z)       # followed by a blank line or end of document\n        )\n        ' % (tab_width - 1), re.X)


_xml_oneliner_re_from_tab_width = _memoized(_xml_oneliner_re_from_tab_width)

def _hr_tag_re_from_tab_width(tab_width):
    return re.compile('\n        (?:\n            (?<=\\n\\n)       # Starting after a blank line\n            |               # or\n            \\A\\n?           # the beginning of the doc\n        )\n        (                       # save in \\1\n            [ ]{0,%d}\n            <(hr)               # start tag = \\2\n            \\b                  # word break\n            ([^<>])*?           # \n            /?>                 # the matching end tag\n            [ \\t]*\n            (?=\\n{2,}|\\Z)       # followed by a blank line or end of document\n        )\n        ' % (tab_width - 1), re.X)


_hr_tag_re_from_tab_width = _memoized(_hr_tag_re_from_tab_width)

def _xml_escape_attr(attr, skip_single_quote=True):
    """Escape the given string for use in an HTML/XML tag attribute.
    
    By default this doesn't bother with escaping `'` to `&#39;`, presuming that
    the tag attribute is surrounded by double quotes.
    """
    escaped = attr.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
    if not skip_single_quote:
        escaped = escaped.replace("'", '&#39;')
    return escaped


def _xml_encode_email_char_at_random(ch):
    r = random()
    if r > 0.9 and ch not in '@_':
        return ch
    else:
        if r < 0.45:
            return '&#%s;' % hex(ord(ch))[1:]
        return '&#%s;' % ord(ch)


class _NoReflowFormatter(optparse.IndentedHelpFormatter):
    """An optparse formatter that does NOT reflow the description."""

    def format_description(self, description):
        return description or ''


def _test():
    import doctest
    doctest.testmod()


def main(argv=None):
    if argv is None:
        argv = sys.argv
    if not logging.root.handlers:
        logging.basicConfig()
    usage = 'usage: %prog [PATHS...]'
    version = '%prog ' + __version__
    parser = optparse.OptionParser(prog='markdown2', usage=usage, version=version, description=cmdln_desc, formatter=_NoReflowFormatter())
    parser.add_option('-v', '--verbose', dest='log_level', action='store_const', const=logging.DEBUG, help='more verbose output')
    parser.add_option('--encoding', help='specify encoding of text content')
    parser.add_option('--html4tags', action='store_true', default=False, help='use HTML 4 style for empty element tags')
    parser.add_option('-s', '--safe', metavar='MODE', dest='safe_mode', help="sanitize literal HTML: 'escape' escapes HTML meta chars, 'replace' replaces with an [HTML_REMOVED] note")
    parser.add_option('-x', '--extras', action='append', help='Turn on specific extra features (not part of the core Markdown spec). See above.')
    parser.add_option('--use-file-vars', help="Look for and use Emacs-style 'markdown-extras' file var to turn on extras. See <http://code.google.com/p/python-markdown2/wiki/Extras>.")
    parser.add_option('--link-patterns-file', help='path to a link pattern file')
    parser.add_option('--self-test', action='store_true', help='run internal self-tests (some doctests)')
    parser.add_option('--compare', action='store_true', help='run against Markdown.pl as well (for testing)')
    parser.set_defaults(log_level=logging.INFO, compare=False, encoding='utf-8', safe_mode=None, use_file_vars=False)
    (opts, paths) = parser.parse_args()
    log.setLevel(opts.log_level)
    if opts.self_test:
        return _test()
    else:
        if opts.extras:
            extras = {}
            for s in opts.extras:
                splitter = re.compile('[,;: ]+')
                for e in splitter.split(s):
                    if '=' in e:
                        (ename, earg) = e.split('=', 1)
                        try:
                            earg = int(earg)
                        except ValueError:
                            pass

                    else:
                        ename, earg = e, None
                    extras[ename] = earg

        else:
            extras = None
        if opts.link_patterns_file:
            link_patterns = []
            f = open(opts.link_patterns_file)
            try:
                for (i, line) in enumerate(f.readlines()):
                    if not line.strip():
                        continue
                    if line.lstrip().startswith('#'):
                        continue
                    try:
                        (pat, href) = line.rstrip().rsplit(None, 1)
                    except ValueError:
                        raise MarkdownError('%s:%d: invalid link pattern line: %r' % (
                         opts.link_patterns_file, i + 1, line))

                    link_patterns.append((
                     _regex_from_encoded_pattern(pat), href))

            finally:
                f.close()

        else:
            link_patterns = None
        from os.path import join, dirname, abspath, exists
        markdown_pl = join(dirname(dirname(abspath(__file__))), 'test', 'Markdown.pl')
        for path in paths:
            if opts.compare:
                print '==== Markdown.pl ===='
                perl_cmd = 'perl %s "%s"' % (markdown_pl, path)
                o = os.popen(perl_cmd)
                perl_html = o.read()
                o.close()
                sys.stdout.write(perl_html)
                print '==== markdown2.py ===='
            html = markdown_path(path, encoding=opts.encoding, html4tags=opts.html4tags, safe_mode=opts.safe_mode, extras=extras, link_patterns=link_patterns, use_file_vars=opts.use_file_vars)
            sys.stdout.write(html.encode(sys.stdout.encoding or 'utf-8', 'xmlcharrefreplace'))
            if extras and 'toc' in extras:
                log.debug('toc_html: ' + html.toc_html.encode(sys.stdout.encoding or 'utf-8', 'xmlcharrefreplace'))
            if opts.compare:
                test_dir = join(dirname(dirname(abspath(__file__))), 'test')
                if exists(join(test_dir, 'test_markdown2.py')):
                    sys.path.insert(0, test_dir)
                    from test_markdown2 import norm_html_from_html
                    norm_html = norm_html_from_html(html)
                    norm_perl_html = norm_html_from_html(perl_html)
                else:
                    norm_html = html
                    norm_perl_html = perl_html
                print '==== match? %r ====' % (norm_perl_html == norm_html)

        return


if __name__ == '__main__':
    sys.exit(main(sys.argv))