# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/browser/comments.py
# Compiled at: 2019-05-17 05:23:01
from plone.app.discussion.browser.comments import CommentForm as BaseForm
from plone.app.discussion.browser.comments import CommentsViewlet as BaseViewlet

class CommentForm(BaseForm):

    def updateWidgets(self):
        super(CommentForm, self).updateWidgets()
        self.widgets['text'].rows = 15

    def updateActions(self):
        super(CommentForm, self).updateActions()
        self.actions['comment'].title = 'Save Comment'
        for k in self.actions.keys():
            self.actions[k].addClass('standardButton')
            self.actions[k].addClass('defaultWFButton')


class CommentsViewlet(BaseViewlet):
    form = CommentForm