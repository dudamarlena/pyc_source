# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/progressbar/events.py
# Compiled at: 2009-09-18 14:53:56
from zope.component.interfaces import ObjectEvent
from zope.interface import implements, Interface
from interfaces import IInitialiseProgressBar, IUpdateProgressEvent

class InitialiseProgressBar(ObjectEvent):
    __module__ = __name__
    implements(IInitialiseProgressBar)


class UpdateProgressEvent(ObjectEvent):
    __module__ = __name__
    implements(IUpdateProgressEvent)


class ProgressBar(object):
    __module__ = __name__

    def __init__(self, context, request, title, description, view=None):
        self.context = context
        self.request = request
        self.title = title
        self.description = description
        self.view = view


class ProgressState(object):
    __module__ = __name__

    def __init__(self, request, progress):
        self.request = request
        self.progress = progress


def init_progress_bar(bar, event):
    view = bar.view
    if view is None:
        view = bar.context.restrictedTraverse('@@collective.progressbar')
    view.title = bar.title
    view.description = bar.description
    bar.request.response.write(view().encode('utf-8'))
    return


def update_progress(state, event):
    state.request.response.write('<input style="display: none;" name="_progress" value="%s">' % state.progress)