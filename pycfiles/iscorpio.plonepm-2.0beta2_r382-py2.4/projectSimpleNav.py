# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/portlets/projectSimpleNav.py
# Compiled at: 2009-10-20 12:55:51
"""
a portlet to provide simple navigation for a project.

list each iteration, all stories, all function requirments, etc.
"""
from zope.interface import implements
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from interfaces import IProjectSimpleNavPortlet
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

class Assignment(base.Assignment):
    """
    persistent data for this portlet.  Let's keep it simple now.
    """
    __module__ = __name__
    implements(IProjectSimpleNavPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        return 'Project Navigation'


class Renderer(base.Renderer):
    """
    returns the HTML for the portlet on page.
    """
    __module__ = __name__
    _template = ViewPageTemplateFile('projectSimpleNav.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        try:
            self.project = aq_inner(self.context).getProjectRoot()
        except AttributeError:
            self.project = None

        return

    def render(self):
        return self._template()

    @property
    def available(self):
        """
        The condition to show this portlet. This portlet will only
        show up within a project context.  It will also show up for all
        contents of a project.
        """
        if not self.project:
            return False
        else:
            return True

    def projectInfo(self):
        return {'url': self.project.absolute_url(), 'title': self.project.title or self.project.id}

    def iterations(self):
        """
        returns the latest active 5 iterations.
        """
        infos = []
        iterations = self.project.xpCatalogSearch(portal_type='PPMIteration', sort_on='modified', sort_order='reverse', sort_limit=5)
        for iteration in iterations:
            obj = iteration.getObject()
            infos.append({'url': obj.absolute_url(), 'title': obj.title or obj.id, 'icon': obj.getIcon()})

        return infos

    def stories(self):
        """
        returns the last 5 recent changed stories.
        """
        values = []
        stories = self.project.xpCatalogSearch(portal_type='PPMStory', sort_on='modified', sort_order='reverse', sort_limit=5)
        for story in stories:
            obj = story.getObject()
            values.append({'url': obj.absolute_url(), 'title': obj.title or obj.id, 'icon': obj.getIcon()})

        return values


class AddForm(base.NullAddForm):
    __module__ = __name__

    def create(self):
        return Assignment()