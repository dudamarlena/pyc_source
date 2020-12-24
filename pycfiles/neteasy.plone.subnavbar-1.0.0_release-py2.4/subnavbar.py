# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neteasy/plone/subnavbar/browser/subnavbar.py
# Compiled at: 2009-01-16 14:42:36
""" neteasy.plone.subnavbar
    Copyright (C) 2008-9, Jim Nelson <jim.nelson@neteasyinc.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from neteasy.plone.subnavbar.navbar_contents import getSecondLevelList

class SubnavbarViewlet(ViewletBase):
    __module__ = __name__
    render = ViewPageTemplateFile('subnavbar.pt')

    def update(self):
        self.contentlist = getSecondLevelList(self.context)