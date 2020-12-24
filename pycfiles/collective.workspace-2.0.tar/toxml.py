# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/workflowed/browser/toxml.py
# Compiled at: 2008-07-25 18:15:12
from zope.component import getUtility
from StringIO import StringIO
from Products.Five.browser import BrowserView
from collective.wtf.interfaces import ICSVWorkflowSerializer
from collective.wtf.exportimport import CSVWorkflowDefinitionConfigurator

class ToXML(BrowserView):
    """Export the context workflow to XML as a one-off
    """
    __module__ = __name__

    def __call__(self):
        wfdc = CSVWorkflowDefinitionConfigurator(self.context)
        xml = wfdc.__of__(self.context).generateWorkflowXML()
        self.request.response.setHeader('Content-type', 'text/xml')
        return xml