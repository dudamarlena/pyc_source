# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/webadmin/categories.py
# Compiled at: 2006-12-26 17:18:01
"""
    pocoo.pkg.webadmin.categories
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: 2006 by Armin Ronacher.
    :license: GNU GPL, see LICENSE for more details.
"""
from pocoo.pkg.webadmin.base import AdminCategory, get_category

class SettingsCategory(AdminCategory):
    __module__ = __name__
    identifier = 'settings'

    def get_title(self, req):
        _ = req.gettext
        return _('Settings')

    def get_description(self, req):
        _ = req.gettext
        return _('Allows you to change general settings like editing the configuration, caching settings etc.')


class ForumCategory(AdminCategory):
    __module__ = __name__
    identifier = 'forum'

    def get_title(self, req):
        _ = req.gettext
        return _('Forum')

    def get_description(self, req):
        _ = req.gettext
        return _('Here you can configure the forums and categories')


class UserCategory(AdminCategory):
    __module__ = __name__
    identifier = 'user'

    def get_title(self, req):
        _ = req.gettext
        return _('User')

    def get_description(self, req):
        _ = req.gettext
        return _('Here you can edit users')