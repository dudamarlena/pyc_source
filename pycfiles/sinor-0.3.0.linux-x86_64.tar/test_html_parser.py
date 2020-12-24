# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mahnve/.virtualenvs/blog/lib/python2.7/site-packages/test/test_html_parser.py
# Compiled at: 2015-02-10 09:08:48
from sinor import html_content
from nose.tools import assert_equals

def test_parse_empty_string():
    assert_equals(html_content.from_string(''), {'title': '', 'date': '', 
       'content': ''})


def test_finds_a_post_title_class():
    html = "<div><div id='post-title'>Title</div></div>"
    assert_equals(html_content.from_string(html), {'title': 'Title', 'date': '', 
       'content': ''})


def test_finds_a_post_date():
    html = "<div><time id='post-date'>2010-01-01</time></div>"
    assert_equals(html_content.from_string(html), {'date': '2010-01-01', 'title': '', 
       'content': ''})


def test_finds_post_content():
    html = '<div id="post-content"><p>Ulysseus!</p></div>'
    assert_equals(html_content.from_string(html), {'content': html, 'title': '', 
       'date': ''})


def test_multihtml():
    html = '<div><div id="post-content"><h1 id="post-title">Foo</h1><time id="post-date">2010-01-01</time></div></div>'
    assert_equals(html_content.from_string(html), {'content': '<div id="post-content"><h1 id="post-title">Foo</h1><time id="post-date">2010-01-01</time></div>', 
       'title': 'Foo', 
       'date': '2010-01-01'})