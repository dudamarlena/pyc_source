# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/transmute/__init__.py
# Compiled at: 2014-02-20 17:18:44
try:
    from transmute._version import __version__
except ImportError:
    __version__ = 'unknown'

import transmute.basket
from transmute.bootstrap import PYPI_BASKET
from transmute.resolver import Resolver
from transmute.s3 import S3Basket
from transmute.transmuter import Transmuter
PYPI_SOURCE = PYPI_BASKET.url
transmute.basket.register_basket(PYPI_BASKET)
transmute.basket.register_basket_factory('s3', S3Basket)
_resolver = Resolver()
add_source = _resolver.add_source
require = _resolver.require

def update(resolver=None):
    if resolver is None:
        resolver = globals()['_resolver']
    tm = Transmuter(resolver.entries)
    tm.transmute()
    return