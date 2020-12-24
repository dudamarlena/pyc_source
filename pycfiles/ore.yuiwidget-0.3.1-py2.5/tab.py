# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/yuiwidget/tab.py
# Compiled at: 2008-09-11 20:30:06
"""

Usage is to utilize this class as a base class of a viewlet manager

"""
from zope.viewlet import manager

class TabViewletManager(manager.ViewletManagerBase):
    """
    we should add support for grouping viewlets.
    """

    def render(self):
        header = '<div class="tabber" id="content-manager">'
        parts = [ '<div class="tabbertab">%s</div>' % v.render() for v in self.viewlets ]
        footer = '</div>'
        return '%s \n %s \n %s' % (header, ('\n').join(parts), footer)