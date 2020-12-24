# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kmike/svn/scrapy-poet/tests/test_middleware.py
# Compiled at: 2020-04-27 13:38:41
# Size of source mod 2**32: 6958 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from scrapy.utils.log import configure_logging
from twisted.internet.defer import returnValue
from twisted.internet.threads import deferToThread
from typing import Optional, Union, Type
import scrapy
from scrapy import Request
from scrapy.http import Response
from pytest_twisted import inlineCallbacks
import attr
from scrapy_poet import callback_for
from web_poet.pages import WebPage, ItemWebPage
from scrapy_poet.page_input_providers import provides, PageObjectInputProvider
from web_poet.page_inputs import ResponseData
from scrapy_poet.utils import DummyResponse
from tests.utils import HtmlResource, crawl_items, capture_exceptions, crawl_single_item

class ProductHtml(HtmlResource):
    html = '\n    <html>\n        <div class="breadcrumbs">\n            <a href="/food">Food</a> / \n            <a href="/food/sweets">Sweets</a>\n        </div>\n        <h1 class="name">Chocolate</h1>\n        <p>Price: <span class="price">22€</span></p>\n        <p class="description">The best chocolate ever</p>\n    </html>\n    '


def spider_for(injectable: Type):

    class InjectableSpider(scrapy.Spider):
        url = None

        def start_requests(self):
            yield Request(self.url, capture_exceptions(callback_for(injectable)))

    return InjectableSpider


@attr.s(auto_attribs=True)
class BreadcrumbsExtraction(WebPage):

    def get(self):
        return {a.css('::text').get():a.attrib['href'] for a in self.css('.breadcrumbs a')}


@attr.s(auto_attribs=True)
class ProductPage(ItemWebPage):
    breadcrumbs: BreadcrumbsExtraction

    def to_item(self):
        return {'url':self.url, 
         'name':self.css('.name::text').get(), 
         'price':self.xpath('//*[@class="price"]/text()').get(), 
         'description':self.css('.description::text').get(), 
         'category':' / '.join(self.breadcrumbs.get().keys())}


@inlineCallbacks
def test_basic_case(settings):
    item, url, _ = yield crawl_single_item(spider_for(ProductPage), ProductHtml, settings)
    @py_assert2 = {'url':url,  'name':'Chocolate',  'price':'22€',  'description':'The best chocolate ever',  'category':'Food / Sweets'}
    @py_assert1 = item == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (item, @py_assert2)) % {'py0':@pytest_ar._saferepr(item) if 'item' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(item) else 'item',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


@attr.s(auto_attribs=True)
class OptionalAndUnionPage(ItemWebPage):
    breadcrumbs: BreadcrumbsExtraction
    opt_check_1: Optional[BreadcrumbsExtraction]
    opt_check_2: Optional[str]
    union_check_1: Union[(BreadcrumbsExtraction, ResponseData)]
    union_check_2: Union[(str, ResponseData)]
    union_check_3: Union[(Optional[str], ResponseData)]
    union_check_4: Union[(None, str, ResponseData)]
    union_check_5: Union[(BreadcrumbsExtraction, None, str)]

    def to_item(self):
        return attr.asdict(self, recurse=False)


@inlineCallbacks
def test_optional_and_unions(settings):
    item, _, _ = yield crawl_single_item(spider_for(OptionalAndUnionPage), ProductHtml, settings)
    @py_assert0 = item['breadcrumbs']
    @py_assert2 = @py_assert0.response
    @py_assert5 = item['response']
    @py_assert4 = @py_assert2 is @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.response\n} is %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = item['opt_check_1']
    @py_assert3 = item['breadcrumbs']
    @py_assert2 = @py_assert0 is @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = item['opt_check_2']
    @py_assert3 = None
    @py_assert2 = @py_assert0 is @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = item['union_check_1']
    @py_assert3 = item['breadcrumbs']
    @py_assert2 = @py_assert0 is @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = item['union_check_2']
    @py_assert3 = item['breadcrumbs']
    @py_assert5 = @py_assert3.response
    @py_assert2 = @py_assert0 is @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py6)s\n{%(py6)s = %(py4)s.response\n}', ), (@py_assert0, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    @py_assert0 = item['union_check_3']
    @py_assert3 = None
    @py_assert2 = @py_assert0 is @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = item['union_check_5']
    @py_assert3 = item['breadcrumbs']
    @py_assert2 = @py_assert0 is @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


@attr.s(auto_attribs=True)
class ProvidedAsyncTest:
    msg: str
    response: ResponseData


@provides(ProvidedAsyncTest)
class ResponseDataProvider(PageObjectInputProvider):

    def __init__(self, response: scrapy.http.Response):
        self.response = response

    @inlineCallbacks
    def __call__(self):
        five = yield deferToThread(lambda : 5)
        raise returnValue(ProvidedAsyncTest(f"Provided {five}!", None))


@attr.s(auto_attribs=True)
class ProvidersPage(ItemWebPage):
    provided: ProvidedAsyncTest

    def to_item(self):
        return attr.asdict(self, recurse=False)


@inlineCallbacks
def test_providers(settings):
    item, _, _ = yield crawl_single_item(spider_for(ProvidersPage), ProductHtml, settings)
    @py_assert0 = item['provided']
    @py_assert2 = @py_assert0.msg
    @py_assert5 = 'Provided 5!'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.msg\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = item['provided']
    @py_assert2 = @py_assert0.response
    @py_assert5 = None
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.response\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None


class MultiArgsCallbackSpider(scrapy.Spider):
    url = None

    def start_requests(self):
        yield Request((self.url), (self.parse), cb_kwargs=dict(cb_arg='arg!'))

    def parse(self, response, product: ProductPage, provided: ProvidedAsyncTest, cb_arg: Optional[str], non_cb_arg: Optional[str]):
        yield {'product':product, 
         'provided':provided, 
         'cb_arg':cb_arg, 
         'non_cb_arg':non_cb_arg}


@inlineCallbacks
def test_multi_args_callbacks(settings):
    item, _, _ = yield crawl_single_item(MultiArgsCallbackSpider, ProductHtml, settings)
    @py_assert1 = item['product']
    @py_assert3 = type(@py_assert1)
    @py_assert5 = @py_assert3 == ProductPage
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py6)s', ), (@py_assert3, ProductPage)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(ProductPage) if 'ProductPage' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ProductPage) else 'ProductPage'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = item['provided']
    @py_assert3 = type(@py_assert1)
    @py_assert5 = @py_assert3 == ProvidedAsyncTest
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py6)s', ), (@py_assert3, ProvidedAsyncTest)) % {'py0':@pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(ProvidedAsyncTest) if 'ProvidedAsyncTest' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ProvidedAsyncTest) else 'ProvidedAsyncTest'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = item['cb_arg']
    @py_assert3 = 'arg!'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = item['non_cb_arg']
    @py_assert3 = None
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


@attr.s(auto_attribs=True)
class UnressolvableProductPage(ProductPage):
    this_is_unresolvable: str


@inlineCallbacks
def test_injection_failure(settings):
    configure_logging(settings)
    items, url, crawler = yield crawl_items(spider_for(UnressolvableProductPage), ProductHtml, settings)
    @py_assert2 = []
    @py_assert1 = items == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (items, @py_assert2)) % {'py0':@pytest_ar._saferepr(items) if 'items' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(items) else 'items',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


class MySpider(scrapy.Spider):
    url = None

    def start_requests(self):
        yield Request(url=(self.url), callback=(self.parse))

    def parse(self, response):
        return {'response': response}


class SkipDownloadSpider(scrapy.Spider):
    url = None

    def start_requests(self):
        yield Request(url=(self.url), callback=(self.parse))

    def parse(self, response: DummyResponse):
        return {'response': response}


@inlineCallbacks
def test_skip_downloads(settings):
    item, url, crawler = yield crawl_single_item(MySpider, ProductHtml, settings)
    @py_assert1 = item['response']
    @py_assert4 = isinstance(@py_assert1, Response)
    @py_assert7 = True
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(Response) if 'Response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Response) else 'Response',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = item['response']
    @py_assert4 = isinstance(@py_assert1, DummyResponse)
    @py_assert7 = False
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(DummyResponse) if 'DummyResponse' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DummyResponse) else 'DummyResponse',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = crawler.stats
    @py_assert3 = @py_assert1.get_stats
    @py_assert5 = @py_assert3()
    @py_assert7 = @py_assert5.get
    @py_assert9 = 'downloader/request_count'
    @py_assert11 = 0
    @py_assert13 = @py_assert7(@py_assert9, @py_assert11)
    @py_assert16 = 1
    @py_assert15 = @py_assert13 == @py_assert16
    if not @py_assert15:
        @py_format18 = @pytest_ar._call_reprcompare(('==', ), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.stats\n}.get_stats\n}()\n}.get\n}(%(py10)s, %(py12)s)\n} == %(py17)s', ), (@py_assert13, @py_assert16)) % {'py0':@pytest_ar._saferepr(crawler) if 'crawler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(crawler) else 'crawler',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py17':@pytest_ar._saferepr(@py_assert16)}
        @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert16 = None
    @py_assert1 = crawler.stats
    @py_assert3 = @py_assert1.get_stats
    @py_assert5 = @py_assert3()
    @py_assert7 = @py_assert5.get
    @py_assert9 = 'downloader/response_count'
    @py_assert11 = 0
    @py_assert13 = @py_assert7(@py_assert9, @py_assert11)
    @py_assert16 = 1
    @py_assert15 = @py_assert13 == @py_assert16
    if not @py_assert15:
        @py_format18 = @pytest_ar._call_reprcompare(('==', ), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.stats\n}.get_stats\n}()\n}.get\n}(%(py10)s, %(py12)s)\n} == %(py17)s', ), (@py_assert13, @py_assert16)) % {'py0':@pytest_ar._saferepr(crawler) if 'crawler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(crawler) else 'crawler',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py17':@pytest_ar._saferepr(@py_assert16)}
        @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert16 = None
    item, url, crawler = yield crawl_single_item(SkipDownloadSpider, ProductHtml, settings)
    @py_assert1 = item['response']
    @py_assert4 = isinstance(@py_assert1, Response)
    @py_assert7 = True
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(Response) if 'Response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Response) else 'Response',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = item['response']
    @py_assert4 = isinstance(@py_assert1, DummyResponse)
    @py_assert7 = True
    @py_assert6 = @py_assert4 is @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('is', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n} is %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(DummyResponse) if 'DummyResponse' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DummyResponse) else 'DummyResponse',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = crawler.stats
    @py_assert3 = @py_assert1.get_stats
    @py_assert5 = @py_assert3()
    @py_assert7 = @py_assert5.get
    @py_assert9 = 'downloader/request_count'
    @py_assert11 = 0
    @py_assert13 = @py_assert7(@py_assert9, @py_assert11)
    @py_assert16 = 0
    @py_assert15 = @py_assert13 == @py_assert16
    if not @py_assert15:
        @py_format18 = @pytest_ar._call_reprcompare(('==', ), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.stats\n}.get_stats\n}()\n}.get\n}(%(py10)s, %(py12)s)\n} == %(py17)s', ), (@py_assert13, @py_assert16)) % {'py0':@pytest_ar._saferepr(crawler) if 'crawler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(crawler) else 'crawler',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py17':@pytest_ar._saferepr(@py_assert16)}
        @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert16 = None
    @py_assert1 = crawler.stats
    @py_assert3 = @py_assert1.get_stats
    @py_assert5 = @py_assert3()
    @py_assert7 = @py_assert5.get
    @py_assert9 = 'downloader/response_count'
    @py_assert11 = 0
    @py_assert13 = @py_assert7(@py_assert9, @py_assert11)
    @py_assert16 = 1
    @py_assert15 = @py_assert13 == @py_assert16
    if not @py_assert15:
        @py_format18 = @pytest_ar._call_reprcompare(('==', ), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.stats\n}.get_stats\n}()\n}.get\n}(%(py10)s, %(py12)s)\n} == %(py17)s', ), (@py_assert13, @py_assert16)) % {'py0':@pytest_ar._saferepr(crawler) if 'crawler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(crawler) else 'crawler',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py17':@pytest_ar._saferepr(@py_assert16)}
        @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert16 = None