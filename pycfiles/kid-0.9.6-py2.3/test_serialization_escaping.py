# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/kid/test/test_serialization_escaping.py
# Compiled at: 2007-07-16 07:02:51
"""Tests exercising text escaping."""
__revision__ = '$Rev: 492 $'
__date__ = '$Date: 2007-07-06 21:38:45 -0400 (Fri, 06 Jul 2007) $'
__author__ = 'David Stanek <dstanek@dstanek.com>'
__copyright__ = 'Copyright 2006, David Stanek'
__license__ = 'MIT <http://www.opensource.org/licenses/mit-license.php>'
from kid.serialization import XMLSerializer, XHTMLSerializer, HTMLSerializer
XML = XMLSerializer
XHTML = XHTMLSerializer
HTML = HTMLSerializer
TEST_CHARS = (
 '<', '>', '"', "'", '&')
TEST_STRINGS = ('str', b'k\x84se')
TEST_COMBO = ('str<"&">str', b"k\x84se<'&'>k\x84se")

def escape_functions():
    """Generator producing escape functions."""
    for serializer in (HTMLSerializer, XMLSerializer, XHTMLSerializer):
        for escape in (serializer.escape_cdata, serializer.escape_attrib):
            yield (serializer, escape)


def do_escape(func, test_chars, result_chars, encoding=None):
    for (x, char) in enumerate(test_chars):
        assert func(char, encoding) == result_chars[x]


def test_escape():
    expected = {XML.escape_cdata: ('&lt;', '>', '"', "'", '&amp;'), XML.escape_attrib: ('&lt;', '>', '&quot;', "'", '&amp;'), XHTML.escape_cdata: ('&lt;', '>', '"', "'", '&amp;'), XHTML.escape_attrib: ('&lt;', '>', '&quot;', "'", '&amp;'), HTML.escape_cdata: ('&lt;', '>', '"', "'", '&amp;'), HTML.escape_attrib: ('<', '>', '&quot;', "'", '&amp;')}
    for (serializer, escape) in escape_functions():
        do_escape(escape, TEST_CHARS, expected[escape])


def test_escape_encoding():
    """Test the encoding part of the escaping functions."""
    ascii_expected = (
     'str', b'k\x84se')
    utf8_expected = ('str', 'k&#132;se')
    for (serializer, escape) in escape_functions():
        do_escape(escape, TEST_STRINGS, ascii_expected)
        do_escape(escape, TEST_STRINGS, utf8_expected, 'utf-8')


def test_escape_encoding_combo():
    ascii_expected = {XML.escape_cdata: ('str&lt;"&amp;">str', b"k\x84se&lt;'&amp;'>k\x84se"), XML.escape_attrib: ('str&lt;&quot;&amp;&quot;>str', b"k\x84se&lt;'&amp;'>k\x84se"), XHTML.escape_cdata: ('str&lt;"&amp;">str', b"k\x84se&lt;'&amp;'>k\x84se"), XHTML.escape_attrib: ('str&lt;&quot;&amp;&quot;>str', b"k\x84se&lt;'&amp;'>k\x84se"), HTML.escape_cdata: ('str&lt;"&amp;">str', b"k\x84se&lt;'&amp;'>k\x84se"), HTML.escape_attrib: ('str<&quot;&amp;&quot;>str', b"k\x84se<'&amp;'>k\x84se")}
    utf8_expected = {XML.escape_cdata: ('str&lt;"&amp;"str', "1k&#132;se&lt;'&amp;'&gt;k&#132;se"), XML.escape_attrib: ('str&lt;&quot;&amp;&quot;>str', "k&#132;se&lt;'&amp;'&gt;k&#132;se"), XHTML.escape_cdata: ('str&lt;"&amp;">str', "k&#132;se&lt;'&amp;'&gt;k&#132;se"), XHTML.escape_attrib: ('str&lt;&quot;&amp;&quot;>str', "k&#132;se&lt;'&amp;'&gt;k&#132;se"), HTML.escape_cdata: ('str&lt;"&amp;">str', "k&#132;se&lt;'&amp;'&gt;k&#132;se"), HTML.escape_attrib: ('str<&quot;&amp;&quot;>str', "k&#132;se&lt;'&amp;'&gt;k&#132;se")}
    for (serializer, escape) in escape_functions():
        do_escape(escape, TEST_COMBO, ascii_expected[escape])
        do_escape(escape, TEST_COMBO, utf8_expected[escape], 'utf-8')


def test_escaping_int():
    for (serializer, escape) in escape_functions():
        try:
            assert escape(1)
        except TypeError, e:
            assert str(e) == 'cannot serialize 1 (type int)'


def test_escaping_nbsp():
    for (serializer, escape) in escape_functions():
        assert escape(b'\xa0', 'ascii') == '&#160;'
        assert escape(b'\xa0', 'ascii', {b'\xa0': 'bingo'}) == 'bingo'