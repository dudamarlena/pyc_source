# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/browser/iteration.py
# Compiled at: 2009-09-24 08:56:42
"""
browser views for project iteration.
"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
__author__ = 'Sean Chen'
__email__ = 'chyxiang@gmail.com'

class IterationView(BrowserView):
    """
    the default view for an iteration.
    """
    __module__ = __name__

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getIterationEstimatedHours(self):
        """
        returns the amount of hours estimated for this iteration.
        """
        context = aq_inner(self.context)
        stories = context.getIterationStories()
        hours = 0
        for story in stories:
            hours = hours + story.getObject().xppm_story_estimated_hours

        return hours

    def getIterationUsedHours(self):
        """
        returns the amount of hours estimated for this iteration.
        """
        context = aq_inner(self.context)
        stories = context.getIterationStories()
        hours = 0
        for story in stories:
            hours = hours + story.getObject().xppm_story_used_hours

        return hours

    def getIterationProgressPercent(self):
        """
        returns the progress status as a percentage for this iteration. 
        """
        context = aq_inner(self.context)
        stories = context.getIterationStories()
        progressPercent = 0
        if len(stories) > 0:
            progress = 0
            for story in stories:
                progress = progress + story.getObject().xppm_story_progress_percent

            progressPercent = progress / len(stories)
        return progressPercent