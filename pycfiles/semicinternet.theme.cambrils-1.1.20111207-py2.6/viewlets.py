# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/semicinternet/theme/cambrils/browser/viewlets.py
# Compiled at: 2011-07-15 04:17:20
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

class GlobalSectionsViewlet(common.GlobalSectionsViewlet):
    render = ViewPageTemplateFile('templates/global_sections.pt')


class SocialPagesViewlet(common.ViewletBase):
    render = ViewPageTemplateFile('templates/social_pages.pt')


class DropdownMenuViewlet(common.ViewletBase):
    render = ViewPageTemplateFile('templates/dropdown_menu.pt')