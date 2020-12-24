# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\i18n\tests\test_utils.py
# Compiled at: 2011-07-14 06:09:19
from turbogears.i18n.utils import *

def test_get_accept_languages():
    assert get_accept_languages('da, en-gb;q=0.8, en;q=0.7') == ['da', 'en_GB', 'en']
    assert get_accept_languages('da;q=0.6, en-gb;q=1.0, en;q=0.7') == ['en_GB', 'en', 'da']