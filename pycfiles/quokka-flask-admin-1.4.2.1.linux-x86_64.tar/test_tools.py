# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/flask_admin/tests/test_tools.py
# Compiled at: 2016-06-26 14:14:34
from nose.tools import eq_, ok_
from flask_admin import tools

def test_encode_decode():
    eq_(tools.iterdecode(tools.iterencode([1, 2, 3])), ('1', '2', '3'))
    eq_(tools.iterdecode(tools.iterencode([',', ',', ','])), (',', ',', ','))
    eq_(tools.iterdecode(tools.iterencode(['.hello.,', ',', ','])), ('.hello.,', ',',
                                                                     ','))
    eq_(tools.iterdecode(tools.iterencode(['.....,,,.,,..,.,,.,'])), ('.....,,,.,,..,.,,.,', ))
    eq_(tools.iterdecode(tools.iterencode([])), tuple())
    ok_(tools.iterdecode('.'))
    eq_(tools.iterdecode(','), ('', ''))