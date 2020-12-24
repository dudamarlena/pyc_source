# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/adverlet/browser/template.py
# Compiled at: 2008-12-22 07:00:12
__license__ = 'GPL v.3'
from zope.component import adapter
from zope.interface import implementer
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.contentprovider.interfaces import IContentProvider
from interfaces import IManageUITemplate, IUndoTemplate

@implementer(IManageUITemplate)
@adapter(IContentProvider, IDefaultBrowserLayer)
def manageUITemplate(*argv):
    return ViewPageTemplateFile('manage.pt')


@implementer(IUndoTemplate)
@adapter(IContentProvider, IDefaultBrowserLayer)
def undoTemplate(*argv):
    return ViewPageTemplateFile('undo.pt')