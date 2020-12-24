# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_staticdirect.py
# Compiled at: 2013-09-23 12:05:53
# Size of source mod 2**32: 376 bytes
from mediagoblin.tools import staticdirect

def test_staticdirect():
    sdirect = staticdirect.StaticDirect({None: '/static/',  'theme': 'http://example.org/themestatic'})
    assert sdirect('css/monkeys.css') == '/static/css/monkeys.css'
    assert sdirect('images/lollerskate.png', 'theme') == 'http://example.org/themestatic/images/lollerskate.png'