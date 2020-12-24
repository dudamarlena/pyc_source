# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\PloneStatCounter\viewlets.py
# Compiled at: 2008-07-07 15:40:26
from zope.component import getUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from interfaces import IStatCounterConfig
from utility import UTILITY_NAME
VARIABLE_TEMPLATE = '\n    sc_project=%(sc_project)s;\n    sc_invisible=%(sc_invisible)s;\n    sc_partition=%(sc_partition)s;\n    sc_security="%(sc_security)s";\n'

class StatCounterViewlet(ViewletBase):
    """A viewlet that renders a snippet of XHTML providing a StatCounter page
    counter on a page.
    """
    __module__ = __name__
    render = ViewPageTemplateFile('statcounter.pt')

    def update(self):
        config = getUtility(IStatCounterConfig, name=UTILITY_NAME)
        self.sc_project = config.sc_project
        self.sc_invisible = config.sc_invisible and 1 or 0
        self.sc_partition = config.sc_partition
        self.sc_security = config.sc_security

    def renderJavascriptVariables(self):
        """Return rendered javascript variables for StatCounter.
        """
        return VARIABLE_TEMPLATE % self.__dict__