# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/webadmin/categories.py
# Compiled at: 2006-12-26 17:18:01
__doc__ = '\n    pocoo.pkg.webadmin.categories\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n    :copyright: 2006 by Armin Ronacher.\n    :license: GNU GPL, see LICENSE for more details.\n'
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