# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/kid/test/test_unicode.py
# Compiled at: 2007-07-16 07:02:51
"""Unicode tests"""
from kid.parser import to_unicode
astr = '†©—'
ustr = astr.decode('utf-8')

def test_to_unicode():
    assert to_unicode(ustr, 'utf-8') == ustr
    assert to_unicode(astr, 'utf-8') == ustr

    class C(object):
        __module__ = __name__

        def __unicode__(self):
            return ustr

    assert to_unicode(C(), 'utf-8') == ustr