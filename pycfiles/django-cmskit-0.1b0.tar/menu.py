# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Sites/senpilic.com.tr/senpilic/recipes/menu.py
# Compiled at: 2012-10-09 11:38:32
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language
from cms.menu_bases import CMSAttachMenu
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from senpilic.recipes.models import Recipe

class RecipesMenu(CMSAttachMenu):
    name = _('Recipes menu')

    def get_nodes(self, request):
        nodes = []
        for recipe in Recipe.objects.published().select_related():
            try:
                node = NavigationNode(recipe.title, recipe.get_absolute_url(), recipe.pk)
                nodes.append(node)
            except:
                pass

        return nodes


menu_pool.register_menu(RecipesMenu)