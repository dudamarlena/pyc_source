# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_auth/cms_menus.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 1677 bytes
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from menus.base import Modifier, NavigationNode
from menus.menu_pool import menu_pool
URL_NAME_TO_TITLE = {'login': _('Login'), 
 'logout': _('Logout'), 
 'password_change': _('Change password'), 
 'password_change_done': _('Change password'), 
 'password_reset': _('Reset pasword'), 
 'password_reset_done': _('Reset pasword'), 
 'password_reset_confirm': _('Reset pasword'), 
 'password_reset_complete': _('Reset pasword'), 
 'register': _('Register')}

@menu_pool.register_modifier
class AuthModifier(Modifier):
    __doc__ = '\n    This modifier adds to breadcrumb all authentication URLs.\n    '

    def modify(self, request: HttpRequest, nodes: NavigationNode, namespace: str, root_id: int, post_cut: bool, breadcrumb: bool) -> NavigationNode:
        if not (breadcrumb and request.resolver_match and request.resolver_match.url_name in URL_NAME_TO_TITLE):
            return nodes
        root_nodes = [node for node in nodes if node.attr.get('is_home')]
        if root_nodes:
            root = root_nodes[0]
        else:
            root = NavigationNode('Home', '/', 'rootnodeid')
            root.selected = True
        title = URL_NAME_TO_TITLE[request.resolver_match.url_name]
        node = NavigationNode(title, request.path, 'extranodeid')
        node.selected = True
        node.parent = root
        root.children = [node]
        return [
         root, node]