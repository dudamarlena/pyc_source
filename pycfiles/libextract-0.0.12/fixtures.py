# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\rodrigo\github\datalib\libextract\tests\fixtures.py
# Compiled at: 2015-05-21 02:03:17
import pytest
from tests import asset_path
from libextract.core import parse_html
FOOS_FILENAME = asset_path('full_of_foos.html')

@pytest.fixture
def foo_file(request):
    fp = open(FOOS_FILENAME, 'rb')
    request.addfinalizer(fp.close)
    return fp


@pytest.fixture
def etree():
    with open(FOOS_FILENAME, 'rb') as (fp):
        return parse_html(fp, encoding='utf8')