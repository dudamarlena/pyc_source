# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii-blog/kii_blog/apps.py
# Compiled at: 2014-12-16 11:40:40
from django.utils.translation import ugettext_lazy as _
from kii.app import core, menu

class App(core.App):
    name = 'kii_blog'
    label = 'blog'
    verbose_name = 'Blog'
    urls = '.urls'
    user_access = True

    def ready(self):
        super(App, self).ready()
        self.menu = menu.MenuNode(route='kii:blog:index', label=_('blog'), icon='fi-pencil', children=[
         menu.MenuNode(route='kii:blog:entry:create', label=_('create'))])