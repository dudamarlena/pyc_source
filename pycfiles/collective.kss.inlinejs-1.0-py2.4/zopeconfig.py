# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/kss/inlinejs/demo/zopeconfig.py
# Compiled at: 2009-05-28 10:57:07
from kss.demo.interfaces import IKSSDemoResource, IKSSSeleniumTestResource
from kss.demo.resource import KSSDemo, KSSSeleniumTestDirectory
from zope.interface import implements

class IResource(IKSSDemoResource, IKSSSeleniumTestResource):
    __module__ = __name__


class KSSDemos(object):
    __module__ = __name__
    implements(IResource)
    demos = ()
    selenium_tests = ()