# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/gacontext/browser/viewlets.py
# Compiled at: 2008-05-20 05:21:26
__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 60983 $'
__version__ = '$Revision: 60983 $'[11:-2]
from zope import component
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFPlone.utils import safe_unicode
from collective.gacontext.interfaces import IGAFinder

class GAViewlet(ViewletBase):
    __module__ = __name__

    def __init__(self, context, request, view, manager):
        super(GAViewlet, self).__init__(context, request, view, manager)
        self.context = context
        self.gafinder = component.queryUtility(IGAFinder)

    def update(self):
        pass

    def render(self):
        """render the webstats snippet"""
        if self.gafinder and self.gafinder(self.context):
            return safe_unicode(self.gafinder(self.context))
        else:
            return ''