# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: _build\bdist.win32\egg\xurrency\tests\test_pyxurrency.py
# Compiled at: 2011-02-28 21:10:50
from minimock import Mock, restore
import xurrency, urllib2
from nose.tools import assert_equals, raises, with_setup

class TestXurrency(object):

    def setUp(self):
        urlopen_result = Mock('urlobject')
        urlopen_result.read = Mock('urlobj.read', returns='\n{"result":{"updated_at":"2010-10-02T02:06:00Z", "value":81,"target":"jpy",\n"base":"eur"}, "code":0, "status":"ok"}\n')
        xurrency.urllib2.urlopen = Mock('urlopen', returns=urlopen_result)

    def tearDown(self):
        restore()

    @with_setup(setUp, tearDown)
    def test_get_rate_one(self):
        pyx = xurrency.Xurrency()
        assert_equals(pyx.get_rate('eur', 'jpy'), 81)

    @with_setup(setUp, tearDown)
    def test_get_rate_decimal(self):
        pyx = xurrency.Xurrency()
        assert_equals(pyx.get_rate('eur', 'jpy', 37.2), 3013.2000000000003)

    @with_setup(teardown=tearDown)
    @raises(xurrency.XurrencyAPIInvalidCurrenciesError)
    def test_get_rate_InvalidCurrenciesError(self):
        urlopen_result = Mock('urlobject')
        urlopen_result.read = Mock('urlobj.read', returns='\n{"code": 2, "message": "Currencies are not valid", "status": "fail"}\n')
        xurrency.urllib2.urlopen = Mock('urlopen', returns=urlopen_result)
        pyx = xurrency.Xurrency()
        assert_equals(pyx.get_rate('eur', 'jpy', 37.2), 3013.2000000000003)

    @with_setup(teardown=tearDown)
    @raises(xurrency.XurrencyAPILimitReachedError)
    def test_get_rate_APILimitReachedError(self):
        urlopen_result = Mock('urlobject')
        urlopen_result.read = Mock('urlobj.read', returns='\n{"code": 3,   "status": "fail",\n  "message":\n  "Limit Reached (10 requests per day). Please adquire a license key"}\n')
        xurrency.urllib2.urlopen = Mock('urlopen', returns=urlopen_result)
        pyx = xurrency.Xurrency()
        assert_equals(pyx.get_rate('eur', 'jpy', 37.2), 3013.2000000000003)

    @with_setup(teardown=tearDown)
    @raises(xurrency.XurrencyAPIInvalidKeyError)
    def test_get_rate_APIInvalidKeyError(self):
        urlopen_result = Mock('urlobject')
        urlopen_result.read = Mock('urlobj.read', returns='\n{"code": 4, "status": "fail",\n  "message": "The api key is not valid"}\n')
        xurrency.urllib2.urlopen = Mock('urlopen', returns=urlopen_result)
        pyx = xurrency.Xurrency()
        assert_equals(pyx.get_rate('eur', 'jpy', 37.2), 3013.2000000000003)

    @with_setup(teardown=tearDown)
    @raises(xurrency.XurrencyError)
    def test_get_rate_XurrencyError(self):
        urlopen_result = Mock('urlobject')
        urlopen_result.read = Mock('urlobj.read', returns='\n{"code": 1, "status": "fail",\n  "message": "Amount should be between 0 and 999999999"}\n')
        xurrency.urllib2.urlopen = Mock('urlopen', returns=urlopen_result)
        pyx = xurrency.Xurrency()
        assert_equals(pyx.get_rate('eur', 'jpy', 37.2), 3013.2000000000003)

    @with_setup(setUp, tearDown)
    @raises(xurrency.XurrencyError)
    def test_get_rate_XurrencyError_InvalidCurrency(self):
        pyx = xurrency.Xurrency()
        assert_equals(pyx.get_rate('invalid', 'jpy', 37.2), 3013.2000000000003)

    @with_setup(teardown=tearDown)
    @raises(xurrency.XurrencyURLError)
    def test_get_rate_URLError(self):
        xurrency.urllib2.urlopen = Mock('urlopen', raises=urllib2.URLError(''))
        pyx = xurrency.Xurrency()
        pyx.get_rate('eur', 'jpy')

    @with_setup(teardown=tearDown)
    @raises(xurrency.XurrencyHTTPError)
    def test_get_rate_HTTPError(self):
        xurrency.urllib2.urlopen = Mock('urlopen', raises=urllib2.HTTPError('url', 401, '', {}, None))
        pyx = xurrency.Xurrency()
        pyx.get_rate('eur', 'jpy')
        return

    @with_setup(setUp, tearDown)
    def test_get_rate_WithValue_InvalidCurrenciesError(self):
        """
        Even if XurrencyAPIInvalidCurrenciesError is returned after execute,
        the value has already been used if it has cached it.
        """
        pyx = xurrency.Xurrency()
        assert_equals(pyx.get_rate('eur', 'jpy', 37.2), 3013.2000000000003)
        urlopen_result = Mock('urlobject')
        urlopen_result.read = Mock('urlobj.read', returns='\n{"code": 4, "status": "fail",\n  "message": "The api key is not valid"}\n')
        assert_equals(pyx.get_rate('eur', 'jpy', 37.2), 3013.2000000000003)