# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/browser/copyfiles.py
# Compiled at: 2019-02-15 13:51:23
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.Five import BrowserView

class CopyFileToAnswer(BrowserView):

    def render(self):
        context = aq_inner(self.context)
        conversation = aq_parent(context)
        answer = aq_parent(conversation)
        file = getattr(context, 'attachment', None)
        candidate_id = file.filename
        while candidate_id in answer.keys():
            candidate_id += '-1'

        filename = answer.invokeFactory(id=candidate_id, type_name='NECDFile', file=file)
        return self.request.response.redirect(context.absolute_url())