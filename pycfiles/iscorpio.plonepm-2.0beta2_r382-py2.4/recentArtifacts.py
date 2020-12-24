# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/portlets/recentArtifacts.py
# Compiled at: 2010-03-09 12:59:28
"""
a small portlets to show the recent changes artifacts: stories, responses,
iterations, etc.
"""
from zope.interface import implements
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from interfaces import IRecentArtifactsPortlet
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

class Assignment(base.Assignment):
    """
    The assignment for this portlet.
    """
    __module__ = __name__
    implements(IRecentArtifactsPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        return 'Recent Artifacts Update'


class Renderer(base.Renderer):
    """
    returns the HTML for the portlet.
    """
    __module__ = __name__
    _template = ViewPageTemplateFile('recentArtifacts.pt')

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
        only available for a project context.
        """
        if not self.project:
            return False
        else:
            return True

    def artifacts(self):
        """
        returns the recent changed items.
        """
        infos = []
        types = [
         'PPMIteration', 'PPMStory', 'PPMFuncReq', 'PPMSysReq', 'PPMUseCase']
        artifacts = self.project.xpCatalogSearch(portal_type=types, sort_on='modified', sort_order='reverse', sort_limit=5)
        for artifact in artifacts:
            obj = artifact.getObject()
            infos.append({'url': obj.absolute_url(), 'modified': obj.modified(), 'title': obj.title or obj.id, 'obj': obj})

        return infos


class AddForm(base.NullAddForm):
    __module__ = __name__

    def create(self):
        return Assignment()