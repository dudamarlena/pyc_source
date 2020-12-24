# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kmike/svn/scrapy-poet/tests/test_middleware.py
# Compiled at: 2020-04-27 13:38:41
# Size of source mod 2**32: 6958 bytes
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
    assert item == {'url':url, 
     'name':'Chocolate', 
     'price':'22€', 
     'description':'The best chocolate ever', 
     'category':'Food / Sweets'}


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
    if not item['breadcrumbs'].response is item['response']:
        raise AssertionError
    else:
        if not item['opt_check_1'] is item['breadcrumbs']:
            raise AssertionError
        else:
            if not item['opt_check_2'] is None:
                raise AssertionError
            else:
                assert item['union_check_1'] is item['breadcrumbs']
                assert item['union_check_2'] is item['breadcrumbs'].response
            assert item['union_check_3'] is None
        assert item['union_check_5'] is item['breadcrumbs']


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
    if not item['provided'].msg == 'Provided 5!':
        raise AssertionError
    elif not item['provided'].response == None:
        raise AssertionError


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
    if not type(item['product']) == ProductPage:
        raise AssertionError
    else:
        if not type(item['provided']) == ProvidedAsyncTest:
            raise AssertionError
        elif not item['cb_arg'] == 'arg!':
            raise AssertionError
        assert item['non_cb_arg'] == None


@attr.s(auto_attribs=True)
class UnressolvableProductPage(ProductPage):
    this_is_unresolvable: str


@inlineCallbacks
def test_injection_failure(settings):
    configure_logging(settings)
    items, url, crawler = yield crawl_items(spider_for(UnressolvableProductPage), ProductHtml, settings)
    assert items == []


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
    if not isinstance(item['response'], Response) is True:
        raise AssertionError
    else:
        if not isinstance(item['response'], DummyResponse) is False:
            raise AssertionError
        else:
            if not crawler.stats.get_stats().get('downloader/request_count', 0) == 1:
                raise AssertionError
            else:
                if not crawler.stats.get_stats().get('downloader/response_count', 0) == 1:
                    raise AssertionError
                else:
                    item, url, crawler = yield crawl_single_item(SkipDownloadSpider, ProductHtml, settings)
                    assert isinstance(item['response'], Response) is True
                assert isinstance(item['response'], DummyResponse) is True
            assert crawler.stats.get_stats().get('downloader/request_count', 0) == 0
        assert crawler.stats.get_stats().get('downloader/response_count', 0) == 1