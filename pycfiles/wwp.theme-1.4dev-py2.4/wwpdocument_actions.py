# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/theme/browser/wwpdocument_actions.py
# Compiled at: 2009-09-25 10:00:22
from plone.app.layout.viewlets.content import DocumentActionsViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class wwpdocument_actions(DocumentActionsViewlet):
    __module__ = __name__
    render = ViewPageTemplateFile('templates/document_actions.pt')