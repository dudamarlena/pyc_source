# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zope2/zodbbrowser/left.py
# Compiled at: 2011-01-13 19:14:28
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
try:
    import json
except ImportError:
    import simplejson as json

class Tree(BrowserView):
    """Contents tree
    """

    def context_tree(self):
        if self.context.__name__ == 'Zope' and self.context.__class__.__name__ == 'Application':
            content_tree = build_tree(self.context, 2)
        else:
            content_tree = build_tree(self.context, 2, 1)
        if type(content_tree) == dict:
            content_tree = [
             content_tree]
        return json.dumps(content_tree, ensure_ascii=True, indent=4)


def build_tree(elem, level=1024, remove_root=0):
    """Levels represents how deep is the tree
        """
    if level <= 0:
        return None
    else:
        level -= 1
        lista = elem.objectValues()
        node = {}
        children = []
        for i in lista:
            result = build_tree(i, level)
            if result:
                children.append(result)

        if remove_root:
            return children
        node['title'] = get_id(elem)
        node['children'] = []
        if len(lista):
            node['key'] = get_id(elem)
            node['isFolder'] = True
            if not len(node['children']):
                node['isLazy'] = True
        node['children'] = children
        return node


def get_id(elem):
    if callable(elem.id):
        result = elem.id()
    else:
        result = elem.id
    if not result:
        result = 'Application'
    return result