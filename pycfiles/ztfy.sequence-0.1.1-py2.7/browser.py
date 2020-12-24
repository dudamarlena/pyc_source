# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sequence/browser.py
# Compiled at: 2012-06-11 15:34:53
from ztfy.sequence.interfaces import ISequentialIntIds
from ztfy.skin.interfaces import IDefaultView, IPropertiesMenuTarget
from ztfy.skin.layer import IZTFYBackLayer
from z3c.form import field
from zope.component import adapts
from zope.interface import implements, Interface
from zope.traversing.browser import absoluteURL
from ztfy.skin.form import EditForm

class SequentialIntIdsUtilityDefaultViewAdapter(object):
    """Sequential ID utility default view adapter"""
    adapts(ISequentialIntIds, IZTFYBackLayer, Interface)
    implements(IDefaultView)

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    @property
    def viewname(self):
        return '@@properties.html'

    def getAbsoluteURL(self):
        return '%s/%s' % (absoluteURL(self.context, self.request), self.viewname)


class SequentialIntIdsUtilityEditForm(EditForm):
    """Sequential ID utility edit form"""
    implements(IPropertiesMenuTarget)
    fields = field.Fields(ISequentialIntIds)