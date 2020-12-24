# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/tests/searchable.py
# Compiled at: 2008-07-24 14:48:01
from zope.interface.verify import verifyObject

class SearchableTests:

    def test_searcheable_interface(self):
        from twiddler.interfaces import ISearchable
        verifyObject(ISearchable, self.s)

    def test_bad_getBy(self):
        try:
            self.s.getBy(x='x', y='y')
        except ValueError:
            pass
        else:
            self.fail('ValueError not raised')

    def test_notfound_getBy(self):
        try:
            self.s.getBy(foo='NotFound!')
        except KeyError:
            pass
        else:
            self.fail('KeyError not raised')

    def test_notfound_getitem(self):
        try:
            self.s['NotFound!']
        except KeyError:
            pass
        else:
            self.fail('KeyError not raised')