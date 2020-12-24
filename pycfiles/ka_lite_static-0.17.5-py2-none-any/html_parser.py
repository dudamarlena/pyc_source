# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/html_parser.py
# Compiled at: 2018-07-11 18:15:30
from django.utils.six.moves import html_parser as _html_parser
import re, sys
current_version = sys.version_info
use_workaround = current_version < (2, 7, 3) or current_version >= (3, 0) and current_version < (3,
                                                                                                 2,
                                                                                                 3)
HTMLParseError = _html_parser.HTMLParseError
if not use_workaround:
    HTMLParser = _html_parser.HTMLParser
else:
    tagfind = re.compile('([a-zA-Z][-.a-zA-Z0-9:_]*)(?:\\s|/(?!>))*')

    class HTMLParser(_html_parser.HTMLParser):
        """
        Patched version of stdlib's HTMLParser with patch from:
        http://bugs.python.org/issue670664
        """

        def __init__(self):
            _html_parser.HTMLParser.__init__(self)
            self.cdata_tag = None
            return

        def set_cdata_mode(self, tag):
            try:
                self.interesting = _html_parser.interesting_cdata
            except AttributeError:
                self.interesting = re.compile('</\\s*%s\\s*>' % tag.lower(), re.I)

            self.cdata_tag = tag.lower()

        def clear_cdata_mode(self):
            self.interesting = _html_parser.interesting_normal
            self.cdata_tag = None
            return

        def parse_starttag(self, i):
            self.__starttag_text = None
            endpos = self.check_for_whole_start_tag(i)
            if endpos < 0:
                return endpos
            else:
                rawdata = self.rawdata
                self.__starttag_text = rawdata[i:endpos]
                attrs = []
                match = tagfind.match(rawdata, i + 1)
                assert match, 'unexpected call to parse_starttag()'
                k = match.end()
                self.lasttag = tag = match.group(1).lower()
                while k < endpos:
                    m = _html_parser.attrfind.match(rawdata, k)
                    if not m:
                        break
                    attrname, rest, attrvalue = m.group(1, 2, 3)
                    if not rest:
                        attrvalue = None
                    elif attrvalue[:1] == "'" == attrvalue[-1:] or attrvalue[:1] == '"' == attrvalue[-1:]:
                        attrvalue = attrvalue[1:-1]
                    if attrvalue:
                        attrvalue = self.unescape(attrvalue)
                    attrs.append((attrname.lower(), attrvalue))
                    k = m.end()

                end = rawdata[k:endpos].strip()
                if end not in ('>', '/>'):
                    lineno, offset = self.getpos()
                    if '\n' in self.__starttag_text:
                        lineno = lineno + self.__starttag_text.count('\n')
                        offset = len(self.__starttag_text) - self.__starttag_text.rfind('\n')
                    else:
                        offset = offset + len(self.__starttag_text)
                    self.error('junk characters in start tag: %r' % (
                     rawdata[k:endpos][:20],))
                if end.endswith('/>'):
                    self.handle_startendtag(tag, attrs)
                else:
                    self.handle_starttag(tag, attrs)
                    if tag in self.CDATA_CONTENT_ELEMENTS:
                        self.set_cdata_mode(tag)
                return endpos

        def parse_endtag(self, i):
            rawdata = self.rawdata
            if not rawdata[i:i + 2] == '</':
                raise AssertionError('unexpected call to parse_endtag')
                match = _html_parser.endendtag.search(rawdata, i + 1)
                return match or -1
            else:
                j = match.end()
                match = _html_parser.endtagfind.match(rawdata, i)
                if not match:
                    if self.cdata_tag is not None:
                        self.handle_data(rawdata[i:j])
                        return j
                    self.error('bad end tag: %r' % (rawdata[i:j],))
                tag = match.group(1).strip()
                if self.cdata_tag is not None:
                    if tag.lower() != self.cdata_tag:
                        self.handle_data(rawdata[i:j])
                        return j
                self.handle_endtag(tag.lower())
                self.clear_cdata_mode()
                return j