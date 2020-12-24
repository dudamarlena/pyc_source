# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/eg/theme/browser/viewlets.py
# Compiled at: 2010-09-02 08:54:41
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common
from plone.app.layout.viewlets.common import ViewletBase

class PathBarViewlet(common.PathBarViewlet):
    """A custom version of the path bar class
    """
    __module__ = __name__
    index = ViewPageTemplateFile('path_bar_ego.pt')