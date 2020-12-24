# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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