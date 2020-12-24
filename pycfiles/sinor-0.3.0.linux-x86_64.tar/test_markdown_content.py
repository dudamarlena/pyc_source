# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mahnve/.virtualenvs/blog/lib/python2.7/site-packages/test/test_markdown_content.py
# Compiled at: 2015-03-31 16:28:48
from sinor import markdown_content
import data_builder
from nose.tools import assert_equals

def test_gets_title():
    assert_equals(markdown_content.from_string('title: hej \n date: 2014-10-01 \n\n Hej')['title'], 'hej')


def test_gets_date():
    assert_equals(markdown_content.from_string('title: hej \n date: 2014-10-01 \n\n Hej')['date'], '2014-10-01')


def test_gets_content():
    assert_equals(markdown_content.from_string('title: hej \n date: 2014-10-01 \n\n Hej')['content'], '<p>Hej</p>')


def test_gets_draft():
    assert_equals(markdown_content.from_string('title: hej \n date: 2014-10-01 \ntags: foo\n      bar\ndraft: true\n\n Hej')['status'], 'draft')


def test_gets_tags():
    assert_equals(markdown_content.from_string('title: hej \ntags: foo\n      bar\ndraft: true')['tags'], [
     'foo', 'bar'])