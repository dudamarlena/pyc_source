# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kmike/svn/scrapy-poet/tests/test_callback_for.py
# Compiled at: 2020-04-27 13:38:41
# Size of source mod 2**32: 3535 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, scrapy, pytest
from scrapy.utils.reqser import request_to_dict
from web_poet.pages import ItemPage, ItemWebPage
from scrapy_poet.utils import callback_for, is_response_going_to_be_used, DummyResponse

class FakeItemPage(ItemPage):

    def to_item(self):
        return 'fake item page'


class FakeItemWebPage(ItemWebPage):

    def to_item(self):
        return 'fake item web page'


class MySpider(scrapy.Spider):
    name = 'my_spider'
    parse_item = callback_for(FakeItemPage)
    parse_web = callback_for(FakeItemWebPage)


def test_callback_for():
    """Simple test case to ensure it works as expected."""
    cb = callback_for(FakeItemPage)
    @py_assert2 = callable(cb)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0':@pytest_ar._saferepr(callable) if 'callable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(callable) else 'callable',  'py1':@pytest_ar._saferepr(cb) if 'cb' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cb) else 'cb',  'py3':@pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    fake_page = FakeItemPage()
    response = DummyResponse('http://example.com/')
    result = cb(response=response, page=fake_page)
    @py_assert2 = list(result)
    @py_assert5 = [
     'fake item page']
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_callback_for_instance_method():
    spider = MySpider()
    response = DummyResponse('http://example.com/')
    fake_page = FakeItemPage()
    result = spider.parse_item(response, page=fake_page)
    @py_assert2 = list(result)
    @py_assert5 = [
     'fake item page']
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_callback_for_inline():
    callback = callback_for(FakeItemPage)
    response = DummyResponse('http://example.com/')
    fake_page = FakeItemPage()
    result = callback(response, page=fake_page)
    @py_assert2 = list(result)
    @py_assert5 = [
     'fake item page']
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_default_callback():
    """Sample request not specifying callback."""
    spider = MySpider()
    request = scrapy.Request('http://example.com/')
    request_dict = request_to_dict(request, spider)
    @py_assert3 = isinstance(request_dict, dict)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(request_dict) if 'request_dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request_dict) else 'request_dict',  'py2':@pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dict) else 'dict',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert0 = request_dict['url']
    @py_assert3 = 'http://example.com/'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = request_dict['callback']
    @py_assert3 = None
    @py_assert2 = @py_assert0 is @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_instance_method_callback():
    """Sample request specifying spider's instance method callback."""
    spider = MySpider()
    request = scrapy.Request('http://example.com/', callback=(spider.parse_item))
    request_dict = request_to_dict(request, spider)
    @py_assert3 = isinstance(request_dict, dict)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(request_dict) if 'request_dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request_dict) else 'request_dict',  'py2':@pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dict) else 'dict',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert0 = request_dict['url']
    @py_assert3 = 'http://example.com/'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = request_dict['callback']
    @py_assert3 = 'parse_item'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = is_response_going_to_be_used(request, spider)
    @py_assert6 = False
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(is_response_going_to_be_used) if 'is_response_going_to_be_used' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_response_going_to_be_used) else 'is_response_going_to_be_used',  'py1':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    request = scrapy.Request('http://example.com/', callback=(spider.parse_web))
    request_dict = request_to_dict(request, spider)
    @py_assert3 = isinstance(request_dict, dict)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(request_dict) if 'request_dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request_dict) else 'request_dict',  'py2':@pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dict) else 'dict',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert0 = request_dict['url']
    @py_assert3 = 'http://example.com/'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = request_dict['callback']
    @py_assert3 = 'parse_web'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = is_response_going_to_be_used(request, spider)
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(is_response_going_to_be_used) if 'is_response_going_to_be_used' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_response_going_to_be_used) else 'is_response_going_to_be_used',  'py1':@pytest_ar._saferepr(request) if 'request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(request) else 'request',  'py2':@pytest_ar._saferepr(spider) if 'spider' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(spider) else 'spider',  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None


def test_inline_callback():
    """Sample request with inline callback."""
    spider = MySpider()
    cb = callback_for(FakeItemPage)
    request = scrapy.Request('http://example.com/', callback=cb)
    with pytest.raises(ValueError) as (exc):
        request_to_dict(request, spider)
    msg = f"Function {cb} is not a method of: {spider}"
    @py_assert2 = exc.value
    @py_assert4 = str(@py_assert2)
    @py_assert6 = @py_assert4 == msg
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.value\n})\n} == %(py7)s', ), (@py_assert4, msg)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(exc) if 'exc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exc) else 'exc',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(msg) if 'msg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg) else 'msg'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None


def test_invalid_subclass():
    """Classes should inherit from ItemPage."""

    class MyClass(object):
        pass

    with pytest.raises(TypeError) as (exc):
        callback_for(MyClass)
    msg = 'MyClass should be a sub-class of ItemPage.'
    @py_assert2 = exc.value
    @py_assert4 = str(@py_assert2)
    @py_assert6 = @py_assert4 == msg
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.value\n})\n} == %(py7)s', ), (@py_assert4, msg)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(exc) if 'exc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exc) else 'exc',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(msg) if 'msg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg) else 'msg'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None


def test_not_implemented_method():
    """Classes should implement to_item method."""

    class MyClass(ItemPage):
        pass

    with pytest.raises(NotImplementedError) as (exc):
        callback_for(MyClass)
    msg = 'MyClass should implement to_item method.'
    @py_assert2 = exc.value
    @py_assert4 = str(@py_assert2)
    @py_assert6 = @py_assert4 == msg
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.value\n})\n} == %(py7)s', ), (@py_assert4, msg)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(exc) if 'exc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exc) else 'exc',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(msg) if 'msg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg) else 'msg'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None