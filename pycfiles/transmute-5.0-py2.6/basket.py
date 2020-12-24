# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/transmute/basket.py
# Compiled at: 2014-02-04 03:22:39
import re
from transmute.bootstrap import Basket
_basket_factory = {}
_basket = {}
_SCHEME_REGEX = re.compile('^[a-z][a-z0-9+.-]*$')

def register_basket_factory(scheme, factory):
    assert _SCHEME_REGEX.match(scheme)
    _basket_factory[scheme] = factory


def register_basket(basket):
    _basket[basket.url] = basket


def _get_basket(url):
    (scheme, colon, _) = url.partition(':')
    if colon and scheme in _basket_factory:
        return _basket_factory[scheme](url)
    return Basket(path=url)


def get_basket(url):
    if url not in _basket:
        _basket[url] = _get_basket(url)
    return _basket[url]