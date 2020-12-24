# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmvttestapp2/modules/tests/views.py
# Compiled at: 2010-05-30 09:35:01
from pysmvt.view import RespondingViewBase, SnippetViewBase, TextTemplatePage, TextTemplateSnippet, HtmlTemplateSnippet, HtmlTemplatePage

class Rvb(RespondingViewBase):

    def default(self):
        self.retval = 'Hello app2!'


class InApp2(RespondingViewBase):

    def default(self):
        self.retval = 'Hello app2!'


class UnderscoreTemplates(HtmlTemplatePage):

    def default(self):
        pass