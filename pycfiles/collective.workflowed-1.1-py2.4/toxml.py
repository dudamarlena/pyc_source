# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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