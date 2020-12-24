# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kmike/svn/scrapy-poet/tests/test_utils.py
# Compiled at: 2020-04-27 13:38:41
# Size of source mod 2**32: 6475 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, attr
from typing import Any, Dict
import scrapy
from scrapy.http import TextResponse
from scrapy_poet.page_input_providers import PageObjectInputProvider, ResponseDataProvider, provides
from web_poet.pages import ItemPage, WebPage
from scrapy_poet.utils import get_callback, is_callback_using_response, is_provider_using_response, is_response_going_to_be_used, DummyResponse

@attr.s(auto_attribs=True)
class DummyProductResponse:
    data: Dict[(str, Any)]


@attr.s(auto_attribs=True)
class FakeProductResponse:
    data: Dict[(str, Any)]


@provides(DummyProductResponse)
class DummyProductProvider(PageObjectInputProvider):

    def __init__(self, response: DummyResponse):
        self.response = response

    def __call__(self):
        data = {'product': {'url':self.response.url, 
                     'name':'Sample'}}
        return DummyProductResponse(data=data)


@provides(FakeProductResponse)
class FakeProductProvider(PageObjectInputProvider):

    def __call__(self):
        data = {'product': {'url':'http://example.com/sample', 
                     'name':'Sample'}}
        return DummyProductResponse(data=data)


class TextProductProvider(ResponseDataProvider):

    def __init__(self, response: TextResponse):
        self.response = response


class StringProductProvider(ResponseDataProvider):

    def __init__(self, response: str):
        self.response = response


@attr.s(auto_attribs=True)
class DummyProductPage(ItemPage):
    response: DummyProductResponse

    @property
    def url(self):
        return self.response.data['product']['url']

    def to_item(self):
        product = self.response.data['product']
        return product


@attr.s(auto_attribs=True)
class FakeProductPage(ItemPage):
    response: FakeProductResponse

    @property
    def url(self):
        return self.response.data['product']['url']

    def to_item(self):
        product = self.response.data['product']
        return product


class BookPage(WebPage):

    def to_item(self):
        pass


class MySpider(scrapy.Spider):
    name = 'foo'

    def parse(self, response):
        pass

    def parse2(self, res):
        pass

    def parse3(self, response: DummyResponse):
        pass

    def parse4(self, res: DummyResponse):
        pass

    def parse5(self, response, book_page: BookPage):
        pass

    def parse6(self, response: DummyResponse, book_page: BookPage):
        pass

    def parse7(self, response, book_page: DummyProductPage):
        pass

    def parse8(self, response: DummyResponse, book_page: DummyProductPage):
        pass

    def parse9(self, response, book_page: FakeProductPage):
        pass

    def parse10(self, response: DummyResponse, book_page: FakeProductPage):
        pass

    def parse11(self, response: TextResponse):
        pass

    def parse12(self, response: TextResponse, book_page: DummyProductPage):
        pass


def test_get_callback():
    spider = MySpider()
    req = scrapy.Request('http://example.com')
    @py_assert3 = get_callback(req, spider)
    @py_assert7 = spider.parse
    @py_assert5 = @py_assert3 == @py_assert7
    if not @py_assert5:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py8)s\n{%(py8)s = %(py6)s.parse\n}', ), (@py_assert3, @py_assert7)) % {'py0':@pytest_ar._saferepr(get_callback) if 'get_callback' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_callback) else 'get_callback',  'py1':@pytest_ar._saferepr(req) if 'req' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(req) else 'req',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert3 = @py_assert5 = @py_assert7 = None
    req = scrapy.Request('http://example.com', spider.parse2)
    @py_assert3 = get_callback(req, spider)
    @py_assert7 = spider.parse2
    @py_assert5 = @py_assert3 == @py_assert7
    if not @py_assert5:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py8)s\n{%(py8)s = %(py6)s.parse2\n}', ), (@py_assert3, @py_assert7)) % {'py0':@pytest_ar._saferepr(get_callback) if 'get_callback' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_callback) else 'get_callback',  'py1':@pytest_ar._saferepr(req) if 'req' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(req) else 'req',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert3 = @py_assert5 = @py_assert7 = None

    def cb(response):
        pass

    req = scrapy.Request('http://example.com', cb)
    @py_assert3 = get_callback(req, spider)
    @py_assert5 = @py_assert3 == cb
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py6)s', ), (@py_assert3, cb)) % {'py0':@pytest_ar._saferepr(get_callback) if 'get_callback' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_callback) else 'get_callback',  'py1':@pytest_ar._saferepr(req) if 'req' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(req) else 'req',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(cb) if 'cb' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cb) else 'cb'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert3 = @py_assert5 = None


def test_is_provider_using_response():
    @py_assert2 = is_provider_using_response(PageObjectInputProvider)
    @py_assert5 = False
    @py_assert4 = @py_assert2 is @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} is %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(is_provider_using_response) if 'is_provider_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_provider_using_response) else 'is_provider_using_response',  'py1':@pytest_ar._saferepr(PageObjectInputProvider) if 'PageObjectInputProvider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(PageObjectInputProvider) else 'PageObjectInputProvider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = is_provider_using_response(ResponseDataProvider)
    @py_assert5 = True
    @py_assert4 = @py_assert2 is @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} is %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(is_provider_using_response) if 'is_provider_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_provider_using_response) else 'is_provider_using_response',  'py1':@pytest_ar._saferepr(ResponseDataProvider) if 'ResponseDataProvider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ResponseDataProvider) else 'ResponseDataProvider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = is_provider_using_response(TextProductProvider)
    @py_assert5 = True
    @py_assert4 = @py_assert2 is @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} is %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(is_provider_using_response) if 'is_provider_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_provider_using_response) else 'is_provider_using_response',  'py1':@pytest_ar._saferepr(TextProductProvider) if 'TextProductProvider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TextProductProvider) else 'TextProductProvider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = is_provider_using_response(DummyProductProvider)
    @py_assert5 = False
    @py_assert4 = @py_assert2 is @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} is %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(is_provider_using_response) if 'is_provider_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_provider_using_response) else 'is_provider_using_response',  'py1':@pytest_ar._saferepr(DummyProductProvider) if 'DummyProductProvider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DummyProductProvider) else 'DummyProductProvider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = is_provider_using_response(FakeProductProvider)
    @py_assert5 = False
    @py_assert4 = @py_assert2 is @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} is %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(is_provider_using_response) if 'is_provider_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_provider_using_response) else 'is_provider_using_response',  'py1':@pytest_ar._saferepr(FakeProductProvider) if 'FakeProductProvider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(FakeProductProvider) else 'FakeProductProvider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = is_provider_using_response(StringProductProvider)
    @py_assert5 = False
    @py_assert4 = @py_assert2 is @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} is %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(is_provider_using_response) if 'is_provider_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_provider_using_response) else 'is_provider_using_response',  'py1':@pytest_ar._saferepr(StringProductProvider) if 'StringProductProvider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(StringProductProvider) else 'StringProductProvider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_is_callback_using_response():
    spider = MySpider()
    @py_assert2 = spider.parse
    @py_assert4 = is_callback_using_response(@py_assert2)
    @py_assert7 = True
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.parse\n})\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(is_callback_using_response) if 'is_callback_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_callback_using_response) else 'is_callback_using_response',  'py1':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = spider.parse2
    @py_assert4 = is_callback_using_response(@py_assert2)
    @py_assert7 = True
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.parse2\n})\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(is_callback_using_response) if 'is_callback_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_callback_using_response) else 'is_callback_using_response',  'py1':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = spider.parse3
    @py_assert4 = is_callback_using_response(@py_assert2)
    @py_assert7 = False
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.parse3\n})\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(is_callback_using_response) if 'is_callback_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_callback_using_response) else 'is_callback_using_response',  'py1':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = spider.parse4
    @py_assert4 = is_callback_using_response(@py_assert2)
    @py_assert7 = False
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.parse4\n})\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(is_callback_using_response) if 'is_callback_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_callback_using_response) else 'is_callback_using_response',  'py1':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = spider.parse5
    @py_assert4 = is_callback_using_response(@py_assert2)
    @py_assert7 = True
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.parse5\n})\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(is_callback_using_response) if 'is_callback_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_callback_using_response) else 'is_callback_using_response',  'py1':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = spider.parse6
    @py_assert4 = is_callback_using_response(@py_assert2)
    @py_assert7 = False
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.parse6\n})\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(is_callback_using_response) if 'is_callback_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_callback_using_response) else 'is_callback_using_response',  'py1':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = spider.parse7
    @py_assert4 = is_callback_using_response(@py_assert2)
    @py_assert7 = True
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.parse7\n})\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(is_callback_using_response) if 'is_callback_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_callback_using_response) else 'is_callback_using_response',  'py1':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = spider.parse8
    @py_assert4 = is_callback_using_response(@py_assert2)
    @py_assert7 = False
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.parse8\n})\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(is_callback_using_response) if 'is_callback_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_callback_using_response) else 'is_callback_using_response',  'py1':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = spider.parse9
    @py_assert4 = is_callback_using_response(@py_assert2)
    @py_assert7 = True
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.parse9\n})\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(is_callback_using_response) if 'is_callback_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_callback_using_response) else 'is_callback_using_response',  'py1':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = spider.parse10
    @py_assert4 = is_callback_using_response(@py_assert2)
    @py_assert7 = False
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.parse10\n})\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(is_callback_using_response) if 'is_callback_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_callback_using_response) else 'is_callback_using_response',  'py1':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = spider.parse11
    @py_assert4 = is_callback_using_response(@py_assert2)
    @py_assert7 = True
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.parse11\n})\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(is_callback_using_response) if 'is_callback_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_callback_using_response) else 'is_callback_using_response',  'py1':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = spider.parse12
    @py_assert4 = is_callback_using_response(@py_assert2)
    @py_assert7 = True
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.parse12\n})\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(is_callback_using_response) if 'is_callback_using_response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_callback_using_response) else 'is_callback_using_response',  'py1':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_is_response_going_to_be_used():
    spider = MySpider()
    request = scrapy.Request('http://example.com')
    @py_assert3 = is_response_going_to_be_used(request, spider)
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(is_response_going_to_be_used) if 'is_response_going_to_be_used' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_response_going_to_be_used) else 'is_response_going_to_be_used',  'py1':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    request = scrapy.Request('http://example.com', callback=(spider.parse2))
    @py_assert3 = is_response_going_to_be_used(request, spider)
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(is_response_going_to_be_used) if 'is_response_going_to_be_used' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_response_going_to_be_used) else 'is_response_going_to_be_used',  'py1':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    request = scrapy.Request('http://example.com', callback=(spider.parse3))
    @py_assert3 = is_response_going_to_be_used(request, spider)
    @py_assert6 = False
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(is_response_going_to_be_used) if 'is_response_going_to_be_used' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_response_going_to_be_used) else 'is_response_going_to_be_used',  'py1':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    request = scrapy.Request('http://example.com', callback=(spider.parse4))
    @py_assert3 = is_response_going_to_be_used(request, spider)
    @py_assert6 = False
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(is_response_going_to_be_used) if 'is_response_going_to_be_used' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_response_going_to_be_used) else 'is_response_going_to_be_used',  'py1':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    request = scrapy.Request('http://example.com', callback=(spider.parse5))
    @py_assert3 = is_response_going_to_be_used(request, spider)
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(is_response_going_to_be_used) if 'is_response_going_to_be_used' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_response_going_to_be_used) else 'is_response_going_to_be_used',  'py1':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    request = scrapy.Request('http://example.com', callback=(spider.parse6))
    @py_assert3 = is_response_going_to_be_used(request, spider)
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(is_response_going_to_be_used) if 'is_response_going_to_be_used' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_response_going_to_be_used) else 'is_response_going_to_be_used',  'py1':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    request = scrapy.Request('http://example.com', callback=(spider.parse7))
    @py_assert3 = is_response_going_to_be_used(request, spider)
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(is_response_going_to_be_used) if 'is_response_going_to_be_used' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_response_going_to_be_used) else 'is_response_going_to_be_used',  'py1':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    request = scrapy.Request('http://example.com', callback=(spider.parse8))
    @py_assert3 = is_response_going_to_be_used(request, spider)
    @py_assert6 = False
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(is_response_going_to_be_used) if 'is_response_going_to_be_used' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_response_going_to_be_used) else 'is_response_going_to_be_used',  'py1':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    request = scrapy.Request('http://example.com', callback=(spider.parse9))
    @py_assert3 = is_response_going_to_be_used(request, spider)
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(is_response_going_to_be_used) if 'is_response_going_to_be_used' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_response_going_to_be_used) else 'is_response_going_to_be_used',  'py1':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    request = scrapy.Request('http://example.com', callback=(spider.parse10))
    @py_assert3 = is_response_going_to_be_used(request, spider)
    @py_assert6 = False
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(is_response_going_to_be_used) if 'is_response_going_to_be_used' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_response_going_to_be_used) else 'is_response_going_to_be_used',  'py1':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    request = scrapy.Request('http://example.com', callback=(spider.parse11))
    @py_assert3 = is_response_going_to_be_used(request, spider)
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(is_response_going_to_be_used) if 'is_response_going_to_be_used' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_response_going_to_be_used) else 'is_response_going_to_be_used',  'py1':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    request = scrapy.Request('http://example.com', callback=(spider.parse12))
    @py_assert3 = is_response_going_to_be_used(request, spider)
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(is_response_going_to_be_used) if 'is_response_going_to_be_used' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_response_going_to_be_used) else 'is_response_going_to_be_used',  'py1':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None