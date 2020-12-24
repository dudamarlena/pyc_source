# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/viewlets/quick_add_comment_form.py
# Compiled at: 2007-10-06 06:19:54
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from iqpp.plone.commenting.browser.comment_form import CommentFormView

class QuickAddCommentFormViewlet(ViewletBase, CommentFormView):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('quick_comment_form.pt')

    def __init__(self, context, request, view, manager):
        """
        """
        super(QuickAddCommentFormViewlet, self).__init__(context, request, view, manager)
        self._errors = {}

    @property
    def available(self):
        """
        """
        action = self.request.get('action', '')
        if action in ('add', 'reply'):
            return False
        url = self.request.get('URL', '')
        if url.endswith('comment_form'):
            return False
        return True