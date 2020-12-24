# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/apps/content/menu.py
# Compiled at: 2015-02-18 13:07:39
# Size of source mod 2**32: 1075 bytes
from __future__ import absolute_import, division
from cms.menu_bases import CMSAttachMenu
from django.utils.translation import ugettext_lazy as _
from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from .models import Article, Issue, Topic

class ContentMenu(CMSAttachMenu):
    name = _('content menu')

    def get_nodes(self, request):
        """ Lays out a hierarchical navigation structure by Topic -> Issue."""
        nodes = []
        for topic in Topic.objects.all():
            node = NavigationNode(topic.name, topic.get_absolute_url(), topic.slug)
            nodes.append(node)
            for issue in topic.issue_set.all():
                node = NavigationNode(issue.name, issue.get_absolute_url(), issue.slug, topic.slug)
                nodes.append(node)

        return nodes


menu_pool.register_menu(ContentMenu)