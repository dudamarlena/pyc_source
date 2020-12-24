# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/victortorres/git/shub/core-po/tests/test_pages.py
# Compiled at: 2020-04-27 10:50:12
# Size of source mod 2**32: 1759 bytes
import pytest
from web_poet.pages import ItemPage, ItemWebPage, is_injectable

def test_abstract_page_object():
    with pytest.raises(TypeError) as (exc):
        ItemPage()
    msg = "Can't instantiate abstract class ItemPage with abstract methods to_item"
    assert str(exc.value) == msg


def test_abstract_web_page_object():
    with pytest.raises(TypeError) as (exc):
        ItemWebPage()
    msg = "Can't instantiate abstract class ItemWebPage with abstract methods to_item"
    assert str(exc.value) == msg


def test_page_object():

    class MyItemPage(ItemPage):

        def to_item(self) -> dict:
            return {'foo': 'bar'}

    page_object = MyItemPage()
    assert page_object.to_item() == {'foo': 'bar'}


def test_web_page_object(book_list_html_response):

    class MyWebPage(ItemWebPage):

        def to_item(self) -> dict:
            return {'url':self.url, 
             'title':self.css('title::text').get().strip()}

    page_object = MyWebPage(book_list_html_response)
    assert page_object.to_item() == {'url':'http://book.toscrape.com/', 
     'title':'All products | Books to Scrape - Sandbox'}


def test_is_injectable():

    class MyClass:
        pass

    class MyItemPage(ItemPage):

        def to_item(self) -> dict:
            return {'foo': 'bar'}

    assert is_injectable(None) is False
    assert is_injectable(MyClass) is False
    assert is_injectable(MyClass()) is False
    assert is_injectable(MyItemPage) is True
    assert is_injectable(MyItemPage()) is False
    assert is_injectable(ItemPage) is True
    assert is_injectable(ItemWebPage) is True