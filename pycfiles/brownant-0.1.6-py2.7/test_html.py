# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/tests/test_pipeline/test_html.py
# Compiled at: 2014-10-08 05:32:06
from __future__ import absolute_import, unicode_literals
from pytest import raises
from mock import patch, Mock
from brownant.pipeline.html import ElementTreeProperty, XPathTextProperty

def test_etree_default_attr_name():
    etree = ElementTreeProperty()
    assert etree.attr_names[b'text_response_attr'] == b'text_response'


def test_etree_default_encoding_show_be_none():
    etree = ElementTreeProperty()
    assert etree.options[b'encoding'] is None
    return


@patch(b'lxml.html.fromstring')
def test_etree_general_parse_with_default(fromstring):
    mock = Mock()
    etree = ElementTreeProperty()
    etree.provide_value(mock)
    fromstring.assert_called_once_with(mock.text_response)


@patch(b'lxml.html.fromstring')
def test_etree_general(fromstring):
    mock = Mock()
    etree = ElementTreeProperty(text_response_attr=b'foo')
    etree.provide_value(mock)
    fromstring.assert_called_once_with(mock.foo)


@patch(b'lxml.html.fromstring')
def test_etree_general_parse_with_encoding(fromstring):
    mock = Mock()
    etree = ElementTreeProperty(text_response_attr=b'foo', encoding=b'utf-8')
    etree.provide_value(mock)
    fromstring.assert_called_once_with(mock.foo.encode(b'utf-8'))


def test_xpath_default_attr_name():
    with raises(TypeError):
        XPathTextProperty()
    text = XPathTextProperty(xpath=b'//path')
    assert text.xpath == b'//path'
    assert text.attr_names[b'etree_attr'] == b'etree'
    assert text.options[b'strip_spaces'] is False
    assert text.options[b'pick_mode'] == b'join'
    assert text.options[b'joiner'] == b' '


def test_xpath_without_spaces():
    mock = Mock()
    mock.tree.xpath.return_value = [b'a', b'b', b'c']
    text = XPathTextProperty(xpath=b'//path', etree_attr=b'tree', pick_mode=b'join', joiner=b'|')
    rv = text.provide_value(mock)
    mock.tree.xpath.assert_called_with(b'//path')
    assert rv == b'a|b|c'
    text = XPathTextProperty(xpath=b'//another-path', etree_attr=b'tree', pick_mode=b'first')
    rv = text.provide_value(mock)
    mock.tree.xpath.assert_called_with(b'//another-path')
    assert rv == b'a'


def test_xpath_with_striping_spaces():
    mock = Mock()
    mock.tree.xpath.return_value = [b' a ', b'\n b \n', b'\n\n c  \t']
    text = XPathTextProperty(xpath=b'//foo-path', etree_attr=b'tree', pick_mode=b'join', strip_spaces=True)
    rv = text.provide_value(mock)
    mock.tree.xpath.assert_called_with(b'//foo-path')
    assert rv == b'a b c'
    text = XPathTextProperty(xpath=b'//bar-path', etree_attr=b'tree', pick_mode=b'first', strip_spaces=True)
    rv = text.provide_value(mock)
    mock.tree.xpath.assert_called_with(b'//bar-path')
    assert rv == b'a'


def test_xpath_keep_pick_mode():
    mock = Mock()
    value = [b'a', b'b', b'c']
    mock.tree.xpath.return_value = value
    text = XPathTextProperty(xpath=b'//foo-path', etree_attr=b'tree', pick_mode=b'keep')
    rv = text.provide_value(mock)
    mock.tree.xpath.assert_called_with(b'//foo-path')
    assert rv == value


def test_xpath_invalid_pick_mode():
    with raises(ValueError) as (excinfo):
        text = XPathTextProperty(xpath=b'//foo-path', pick_mode=b'unknown')
        text.provide_value(Mock())
    assert b'unknown' in repr(excinfo.value)