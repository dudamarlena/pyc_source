# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\rodrigo\github\libextract\libextract\tests\conftest.py
# Compiled at: 2015-04-12 05:12:58
from pytest import fixture
from tests import asset_path
from libextract.coretools import parse_html
FOOS_FILENAME = asset_path('full_of_foos.html')

@fixture
def foo_file(request):
    fp = open(FOOS_FILENAME, 'rb')
    request.addfinalizer(fp.close)
    return fp


@fixture
def etree(foo_file):
    return parse_html(foo_file)