# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/cu3er/browser/views.py
# Compiled at: 2010-05-22 18:32:52
from zope.component import getMultiAdapter
from Products.Five.browser import BrowserView

class CU3ERXML(BrowserView):
    """XML configuration."""

    def __call__(self, request=None, response=None):
        """Returns config.xml for CU3ER."""
        self.request.response.setHeader('Content-type', 'text/xml')
        self.parent_context = None
        cstate = getMultiAdapter((self.context, self.request), name='plone_context_state')
        if not cstate.is_default_page() and self.context.getDefaultPage():
            self.parent_context = self.context
            self.context = self.context[self.context.getDefaultPage()]
        schema = getattr(self.context, 'Schema', None)
        if schema is None:
            return
        else:
            field = schema().getField('cu3er_config')
            if field is None:
                return
            return field.getRaw(self.context)