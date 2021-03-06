# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/portlets/projectOverview.py
# Compiled at: 2010-03-13 15:42:46
"""
the project overview portlet will provide overview
information for project: project homepage, all stories list,
all metadata list, all releases list, roadmap, source code
repository, source code repository web view, etc.
"""
from zope.interface import implements
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from interfaces import IProjectOverviewPortlet
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

class Assignment(base.Assignment):
    """
    a project's overview info.
    """
    __module__ = __name__
    implements(IProjectOverviewPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        return 'Project Overview'


class Renderer(base.Renderer):
    """
    returns the HTML for this portlet.
    """
    __module__ = __name__
    _template = ViewPageTemplateFile('projectOverview.pt')

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
        this portlet should be only avaialable for a project and
        its contents.
        """
        if not self.project:
            return False
        else:
            return True

    def projectInfo(self):
        """
        basic information for a project: homepage, all metadata,
        all releae, stories,etc.
        TODO: make the view configuration.
        """
        projectUrl = self.project.absolute_url()
        return {'url': projectUrl, 'projectUrl': projectUrl + '/project_view', 'iterationsUrl': projectUrl + '/project_iterations', 'storiesUrl': projectUrl + '/project_stories', 'useCasesUrl': projectUrl + '/project_useCases', 'title': self.project.title or self.project.id, 'svnUrl': self.project.xppm_repo_url, 'viewUrl': self.project.xppm_browse_code_url, 'storiesAmount': len(self.project.getAllStories()), 'useCasesAmount': len(self.project.getAllUseCases()), 'iterationsAmount': len(self.project.getAllIterations())}


class AddForm(base.NullAddForm):
    __module__ = __name__

    def create(self):
        return Assignment()