# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/adi/fullscreen/browser/viewlets.py
# Compiled at: 2013-03-10 07:52:05
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

class SiteFullscreenViewlet(ViewletBase):
    render = ViewPageTemplateFile('toggle_sitefullscreen.pt')