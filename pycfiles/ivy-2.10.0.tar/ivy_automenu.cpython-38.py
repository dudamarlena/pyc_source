# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmulholl/dev/src/ivy/ivy/extensions/ivy_automenu.py
# Compiled at: 2020-04-04 13:34:48
# Size of source mod 2**32: 2252 bytes
import ivy
cache = None

@ivy.hooks.register('render_page')
def add_automenu(page):
    global cache
    if cache is None:
        cache = get_pagelist()
    page['automenu'] = cache


def get_pagelist():
    menu = [
     '<ul>\n']
    root = ivy.nodes.root()
    title = root.get('menu_title') or root.get('title') or 'Home'
    menu.append('<li><a href="@root/">%s</a></li>\n' % title)
    for child in sorted_children(root):
        if not child.empty:
            if not child.get('menu_exclude', False):
                add_node(child, menu)
        menu.append('</ul>')
        return ''.join(menu)


def add_node(node, menu):
    menu.append('<li>')
    title = node.get('menu_title') or node.get('title') or 'Untitled Node'
    menu.append('<a href="%s">%s</a>' % (node.url, title))
    if node.has_children:
        menu_children = []
        for child in sorted_children(node):
            if not child.empty:
                if not child.get('menu_exclude', False):
                    menu_children.append(child)
        else:
            if menu_children:
                menu.append('<ul>\n')
                for child in menu_children:
                    add_node(child, menu)
                else:
                    menu.append('</ul>\n')

    menu.append('</li>\n')


def sorted_children(node):
    return sorted((node.childlist), key=(lambda n: n.get('menu_order', 0)))