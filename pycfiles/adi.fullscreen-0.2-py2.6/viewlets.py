# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/adi/fullscreen/browser/viewlets.py
# Compiled at: 2013-03-10 07:52:05
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

class SiteFullscreenViewlet(ViewletBase):
    render = ViewPageTemplateFile('toggle_sitefullscreen.pt')