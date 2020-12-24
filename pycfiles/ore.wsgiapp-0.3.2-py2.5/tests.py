# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/wsgiapp/tests.py
# Compiled at: 2008-05-01 10:27:18
import re, unittest, os
from zope.testing import doctest, renormalizing
from zope.app.testing import placelesssetup, ztapi
from ore.wsgiapp.app import Application
test_zcml_contents = open(os.path.join(os.path.dirname(__file__), 'test.zcml'))

class TestApplication(Application):
    """ a really simple containerish application """
    pass


class AppView(object):
    """ a simple view we register for the application """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return 'Hello World'


def test_suite():
    ns = dict(component=ztapi, test_zcml_contents=test_zcml_contents)
    return unittest.TestSuite((
     doctest.DocFileSuite('readme.txt', checker=renormalizing.RENormalizing([
      (
       re.compile('at 0x[0-9a-f]+'), 'at <SOME ADDRESS>')])),))