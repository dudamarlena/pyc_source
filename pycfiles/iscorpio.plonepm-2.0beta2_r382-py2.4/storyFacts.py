# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/portlets/storyFacts.py
# Compiled at: 2010-03-19 03:42:29
"""
Story facts portlet will show the summary, iterations plan,
dependence storie, etc about a story.
"""
from zope.interface import implements
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from interfaces import IStoryFactsPortlet
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

class Assignment(base.Assignment):
    """
    persist the properties for this portlet.
    """
    __module__ = __name__
    implements(IStoryFactsPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        return 'Story Facts'


class Renderer(base.Renderer):
    """
    returns all needs for render the portlet on page.
    """
    __module__ = __name__
    _template = ViewPageTemplateFile('storyFacts.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        try:
            self.story = aq_inner(self.context).getStoryRoot()
        except AttributeError:
            self.story = None

        return

    def render(self):
        return self._template()

    @property
    def available(self):
        """
        Only available for story and its contents
        """
        if not self.story:
            return False
        elif self.story.absolute_url().rfind('portal_factory') > -1:
            return False
        else:
            return True

    def storyInfo(self):
        """
        returns story title, url, hour usage, status, etc.
        """
        iteration = self.story.getIteration(self.story.getXppm_iteration())
        return {'url': self.story.absolute_url(), 'title': self.story.title or self.story.id, 'estimatedHours': self.story.getXppm_story_estimated_hours(), 'usedHours': self.story.getXppm_story_used_hours(), 'progressPercent': self.story.getXppm_story_progress_percent(), 'iterationTitle': iteration.title or iteration.id, 'iterationUrl': iteration.absolute_url(), 'iteration': iteration}

    def useCases(self):
        """
        return a list of use cases associated with this story.
        """
        caseIds = self.story.getXppm_use_cases()
        if caseIds:
            cases = []
            for caseId in caseIds:
                case = self.story.getUseCase(caseId)
                cases.append({'url': case.absolute_url(), 'title': case.title or case.id, 'obj': case})

            return cases
        else:
            return
        return

    def dependencyStories(self):
        """
        all dependence stories for current story.
        """
        values = []
        storyIds = self.story.getXppm_story_dependencies()
        for storyId in storyIds:
            storyObj = self.story.getStory(storyId)
            values.append({'url': storyObj.absolute_url(), 'title': storyObj.title or storyObj.id, 'obj': storyObj})

        return values

    def colleagueStories(self):
        """
        all stories within the same iteration except itself.
        """
        values = []
        stories = self.story.getAllStories(self.story.getXppm_iteration())
        for story in stories:
            obj = story.getObject()
            values.append({'url': obj.absolute_url(), 'title': obj.title or obj.id, 'obj': obj, 'isSelf': obj.id == self.story.id})

        return values


class AddForm(base.NullAddForm):
    __module__ = __name__

    def create(self):
        return Assignment()