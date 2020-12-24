# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/action/twitter/tests.py
# Compiled at: 2010-05-03 04:55:40
import unittest
from zope.testing import doctestunit
from zope.component import testing
from zope.component.interfaces import IObjectEvent
from Testing import ZopeTestCase as ztc
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleAction
from plone.contentrules.rule.interfaces import IExecutable
from plone.app.contentrules.rule import Rule
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()
import collective.action.twitter
from collective.action.twitter import TwitterPublishActionAddForm
from collective.action.twitter import TwitterPublishActionEditForm

class DummyEvent(object):
    __module__ = __name__
    implements(IObjectEvent)

    def __init__(self, object):
        self.object = object


class TestCase(ptc.PloneTestCase):
    __module__ = __name__

    class layer(PloneSite):
        __module__ = __name__

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', collective.action.twitter)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def testRegistered(self):
        element = getUtility(IRuleAction, name='collective.action.twitter.twitteraction')
        self.assertEquals('collective.action.twitter.twitteraction', element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)
        return


def test_suite():
    return unittest.TestSuite([])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')