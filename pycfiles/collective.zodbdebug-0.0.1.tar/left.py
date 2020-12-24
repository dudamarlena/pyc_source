# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/zodbbrowser/left.py
# Compiled at: 2011-09-30 16:33:48
from collective.zodbbrowser.utils import DoomedBrowserView
try:
    import json
except ImportError:
    import simplejson as json

class Tree(DoomedBrowserView):
    """Contents tree
    """

    def context_tree(self):
        smart_filter = self.context.REQUEST.get('smart_filter', None) != 'disabled' and True or False
        if self.context.__name__ == 'Zope' and self.context.__class__.__name__ == 'Application':
            content_tree = build_tree(self.context, 2, smart_filter=smart_filter)
        else:
            content_tree = build_tree(self.context, 2, 1, smart_filter=smart_filter)
        if type(content_tree) == dict:
            content_tree = [
             content_tree]
        return json.dumps(content_tree, ensure_ascii=True, indent=4)


def build_tree(elem, level=1024, remove_root=0, smart_filter=True):
    """Levels represents how deep the tree is
        """
    if level <= 0:
        return
    else:
        level -= 1
        filterThese = getIgnorableObjects()
        lista = elem.objectValues()
        node = {}
        children = []
        result = None
        for i in lista:
            try:
                iid = str(i.id)
            except TypeError:
                continue

            if smart_filter and (iid in filterThese or iid.count('portal_')):
                continue
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


def getIgnorableObjects():
    return [
     'Control_Panel',
     'temp_folder',
     'session_data_manager',
     'browser_id_manager',
     'error_log',
     'standard_error_message',
     'virtual_hosting',
     'acl_users',
     'portal_setup',
     'MailHost',
     'caching_policy_manager',
     'content_type_registry',
     'plone_utils',
     'plone_actionicons',
     'translation_service',
     'mimetypes_registry',
     'archetype_tool',
     'reference_catalog',
     'uid_catalog',
     'HTTPCache',
     'RAMCache',
     'ResourceRegistryCache']