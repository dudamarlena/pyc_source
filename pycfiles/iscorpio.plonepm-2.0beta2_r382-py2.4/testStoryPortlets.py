# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/tests/testStoryPortlets.py
# Compiled at: 2009-11-12 19:29:35
"""
testing the portlets for PPMStory
"""
import unittest
from iscorpio.plonepm.portlets import storyFacts
from base import PlonepmPortletTestCase
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

class TestStoryPortlets(PlonepmPortletTestCase):
    __module__ = __name__

    def testRenderer(self):
        renderer = self.renderer(context=self.folder, assignment=storyFacts.Assignment())
        self.failIf(renderer.available)
        self.failUnless(isinstance(renderer, storyFacts.Renderer))


class TestStoryFactsRenderer(PlonepmPortletTestCase):
    __module__ = __name__

    def testAvailable(self):
        renderer = self.renderer(assignment=storyFacts.Assignment())
        self.failIf(renderer.available)
        self.portal.invokeFactory('PPMProject', 'project1')
        project = getattr(self.portal, 'project1')
        renderer = self.renderer(context=project, assignment=storyFacts.Assignment())
        self.failIf(renderer.available)
        project.invokeFactory('PPMMetadata', 'meta1')
        metadata = getattr(project, 'meta1')
        renderer = self.renderer(context=metadata, assignment=storyFacts.Assignment())
        self.failIf(renderer.available)
        project.invokeFactory('PPMStory', 'story1')
        story1 = getattr(project, 'story1')
        renderer = self.renderer(context=story1, assignment=storyFacts.Assignment())
        self.failUnless(renderer.available)

    def testStoryInfo(self):
        self.portal.invokeFactory('PPMProject', 'project1')
        project1 = getattr(self.portal, 'project1')
        project1.invokeFactory('PPMIteration', 'iter1', title='Iteration Title')
        iter1 = getattr(project1, 'iter1')
        project1.invokeFactory('PPMStory', 'story1', title='Story Title')
        story1 = getattr(project1, 'story1')
        story1.xppm_iteration = 'iter1'
        renderer = self.renderer(context=story1, assignment=storyFacts.Assignment())
        info = renderer.storyInfo()
        self.assertEquals(info['url'], story1.absolute_url())
        self.assertEquals(info['title'], 'Story Title')
        self.assertEquals(info['iterationTitle'], 'Iteration Title')
        self.assertEquals(info['iterationUrl'], iter1.absolute_url())
        self.assertEquals(info['iterationIcon'], iter1.getIcon())

    def testColleagueStories(self):
        self.portal.invokeFactory('PPMProject', 'project1')
        project1 = getattr(self.portal, 'project1')
        project1.invokeFactory('PPMIteration', 'iter1', title='Iteration Title')
        iter1 = getattr(project1, 'iter1')
        project1.invokeFactory('PPMStory', 'story1')
        story1 = getattr(project1, 'story1')
        story1.xppm_iteration = 'iter1'
        self.portal.portal_catalog.indexObject(story1)
        project1.invokeFactory('PPMStory', 'story2')
        story2 = getattr(project1, 'story2')
        story2.xppm_iteration = 'iter1'
        self.portal.portal_catalog.indexObject(story2)
        project1.invokeFactory('PPMStory', 'story3')
        story3 = getattr(project1, 'story3')
        story3.xppm_iteration = 'iter1'
        self.portal.portal_catalog.indexObject(story3)
        renderer = self.renderer(context=story2, assignment=storyFacts.Assignment())
        stories = renderer.colleagueStories()
        self.assertEquals(len(stories), 3)
        self.assertEquals(stories[0]['url'], story1.absolute_url())
        self.assertEquals(stories[1]['title'], story2.id)
        self.assertEquals(stories[2]['url'], story3.absolute_url())


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestStoryPortlets))
    suite.addTest(unittest.makeSuite(TestStoryFactsRenderer))
    return suite