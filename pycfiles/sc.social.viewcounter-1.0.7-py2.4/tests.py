# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-fat/egg/sc/social/viewcounter/tests/tests.py
# Compiled at: 2010-08-18 13:21:09
import unittest, doctest
from datetime import datetime
from datetime import timedelta
from zope.testing import doctestunit
from zope.component import testing, queryUtility
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup
from Products.CMFPlone.utils import getToolByName
from sc.social.viewcounter.pageview import Base
from sc.social.viewcounter.pageview import SCOPED_SESSION_NAME
from sc.social.viewcounter.pageview import session
from sc.social.viewcounter.pageview import PageView
from zope.app.cache.interfaces.ram import IRAMCache
import sc.social.viewcounter

def InvalidateCache(function_name):
    cache = queryUtility(IRAMCache)
    if cache:
        cache.invalidate(function_name)


@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    zcml.load_config('testing.zcml', sc.social.viewcounter.tests)
    zcml.load_config('configure.zcml', sc.social.viewcounter)
    fiveconfigure.debug_mode = False


setup_product()
ptc.setupPloneSite(extension_profiles=['sc.social.viewcounter:default'])

class TestCase(ptc.PloneTestCase):
    __module__ = __name__
    baseContents = []

    def afterSetUp(self):
        """
        """
        objects = []
        self.loginAsPortalOwner()
        baseObject = self.portal
        for typeName in ['News Item', 'Document']:
            objects.extend(self.createBaseContent(baseObject, typeName, quantity=5))

        self.baseContents = [ (o.UID(), ('/').join(o.getPhysicalPath()), o.portal_type) for o in objects ]

    def createBaseContent(self, parent, typeName='News Item', quantity=5):
        """ 
        """
        wt = getToolByName(parent, 'portal_workflow')
        objects = []
        for item in range(quantity):
            oId = '%s_%04d' % (typeName, item)
            oTitle = oId
            oId = parent.invokeFactory(typeName, id=oId, title=oTitle)
            oContent = parent[oId]
            if item % 2:
                oContent.setSubject(['odd content'])
            else:
                oContent.setSubject(['even content'])
            oContent.reindexObject()
            wt.doActionFor(oContent, 'publish')
            objects.append(oContent)

        return objects

    def invalidateReportCache(self):
        """Invalidate report cache
        """
        InvalidateCache('sc.social.viewcounter.browser.viewcounter._reportPageViews')

    def populateViewCounter(self, cleanBefore=False, periods=[], invalidate=True):
        """ Populate viewcounter database
            in order to have data for this test
        """
        contents = self.baseContents
        testSession = session()
        if cleanBefore:
            Base.metadata.drop_all(bind=testSession.bind)
            Base.metadata.create_all(bind=testSession.bind)
        vcBrowserView = self.portal.restrictedTraverse('vc_reports')
        contents = zip(range(len(self.baseContents), 0, -1), contents)
        user_name = 'foo'
        user_ip = '42.42.42.42'
        if not periods:
            periods = [
             'lastHour', 'lastDay', 'lastWeek', 'lastMonth']
        for period in periods:
            timeRange = getattr(vcBrowserView, period)
            (tStart, tEnd) = timeRange
            seconds = (tEnd - tStart).days * 86400 + (tEnd - tStart).seconds
            accesses = []
            for (mult, content) in contents:
                (object_uid, object_path, object_type) = content
                accesses.extend([ (tStart + timedelta(seconds=seconds / mult * i),
                 PageView(object_uid, object_path, object_type, user_ip, user_name))
                 for i in range(1, mult) ])
                for access in accesses:
                    (dt, pv) = access
                    pv.access_datetime = dt
                    testSession.add(pv)

        if invalidate:
            self.invalidateReportCache()

    class layer(PloneSite):
        __module__ = __name__

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([ztc.ZopeDocFileSuite('docs/integration.txt', package='sc.social.viewcounter', test_class=TestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE), ztc.ZopeDocFileSuite('docs/caching.txt', package='sc.social.viewcounter', test_class=TestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE), ztc.ZopeDocFileSuite('docs/portlet.txt', package='sc.social.viewcounter', test_class=TestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE), ztc.FunctionalDocFileSuite('docs/browser.txt', package='sc.social.viewcounter', test_class=TestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')