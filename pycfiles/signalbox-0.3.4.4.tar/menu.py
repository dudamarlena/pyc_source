# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/menu.py
# Compiled at: 2014-08-27 19:26:12
from django.core.urlresolvers import reverse
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _

class SignalBoxMenu(Menu):

    def get_nodes(self, request):
        nodes = []
        if request.user.is_staff:
            nodes.insert(0, NavigationNode('Admin site', reverse('admin:index'), 1))
        return nodes


menu_pool.register_menu(SignalBoxMenu)