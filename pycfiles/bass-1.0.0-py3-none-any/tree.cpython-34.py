# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/bass/tree.py
# Compiled at: 2015-09-13 03:59:27
# Size of source mod 2**32: 7653 bytes
"""
bass.tree
-----
Objects and functions related to the site tree.
"""
import logging, shutil, sys
from copy import copy
from os import mkdir
from os.path import join, splitext
from . import setting
from .common import read_file, read_yaml_string, write_file
from .event import event

class Node:
    __doc__ = 'Node is the base class for Folder, Page and Asset\n       Instance variables:\n           - key: type of node\n           - id: identifier of node (usually unique within tree)\n           - name: name of node (last part of path)\n           - path: path of node\n           - parent: parent node\n           - children: list of child nodes\n\n       Instance methods:\n           - render: abstract method\n           - root: find root of tree\n    '

    def __init__(self, name, path, parent=None):
        """construct Node with given name, path and parent"""
        self.key = ''
        self.id = ''
        self.name = name
        self.path = path
        self.parent = parent
        self.children = []
        self.tags = []

    def ready(self):
        """abstract ready method"""
        pass

    def render(self):
        """abstract render method"""
        pass

    def add(self, node):
        """add child node"""
        node.parent = self
        self.children.append(node)

    def root(self):
        """find root of tree in which this node lives"""
        this = self
        while this.parent is not None:
            this = this.parent

        return this


class Folder(Node):

    def __init__(self, name, path, parent):
        """create new Folder node"""
        super().__init__(name, path, parent)
        self.key = 'Folder'

    def asset(self, name):
        """return asset node with given name in this folder"""
        matches = [child for child in self.children if child.name == name and child.key == 'Asset']
        if matches:
            return matches[0]

    def assets(self):
        """return all asset nodes in this folder"""
        return [child.name for child in self.children if child.key == 'Asset']

    def folder(self, name):
        """return folder node with given name in this folder"""
        matches = [child for child in self.children if child.name == name and child.key == 'Folder']
        if matches:
            return matches[0]

    def folders(self):
        """return all folder nodes in this folder"""
        return [child for child in self.children if child.key == 'Folder']

    def page(self, name):
        """return page node with given name in this folder"""
        matches = [child for child in self.children if child.name == name and child.key == 'Page']
        if matches:
            return matches[0]

    def _pages(self, deep=False):
        result = [node for node in self.children if node.key == 'Page']
        if deep:
            for f in self.folders():
                result.extend(f._pages(deep=True))

        return result

    def pages(self, tag=None, idref=None, deep=False, key='name'):
        """return page nodes with given tag in this folder"""
        result = self._pages(deep=deep)
        if tag:
            result = [node for node in result if tag in node.tags]
        elif idref:
            result = [node for node in result if idref == node.id]
        return sorted(result, key=lambda page: getattr(page, key))

    def ready(self):
        """folder is ready: send event(s)"""
        if self.name == '':
            event('generate:post:root', self)
        else:
            event('generate:post:folder:path:' + self.path, self)

    def render(self):
        """render folder"""
        event('render:pre:root' if self.name == '' else 'render:pre:folder:path:' + self.path, self)
        if self.name != '':
            mkdir(join(setting.output, self.path))
        for node in self.children:
            node.render()

        event('render:post:root' if self.name == '' else 'render:post:folder:path:' + self.path, self)


class Page(Node):

    def __init__(self, name, path, parent):
        """create new Page node; set content, preview and meta attributes"""
        super().__init__(name, path, parent)
        self.key = 'Page'
        self.skin = ''
        full_path = join(setting.input, path)
        self.meta, self.preview, self.content = read_page(full_path)

    def copy(self, sep='_'):
        """create copy of page node, with its own name, path and URL, and empty children list"""
        newpage = copy(self)
        newpage.children = []
        pagename, suffix = splitext(newpage.path)
        newpage.name += sep
        newpage.path = pagename + sep + suffix
        newpage.url = '/' + pagename + sep + '.html'
        return newpage

    def ready(self):
        """page is ready: send event(s)"""
        suffix = splitext(self.path)[1][1:]
        event('generate:post:page:path:' + self.path, self)
        event('generate:post:page:extension:' + suffix, self)

    def render(self):
        """render Page node"""
        event('render:pre:page:any', self)
        event('render:pre:page:path:' + self.path, self)
        if self.id:
            event('render:pre:page:id:' + self.id, self)
        for tag in self.tags:
            event('render:pre:page:tag:' + tag, self)

        if self.skin in setting.template:
            template = setting.template[self.skin]
        else:
            logging.critical("Template '%s' for page %s not available.", self.skin, self.path)
            sys.exit(1)
        write_file(template.render(this=self), join(setting.output, self.url[1:]))
        for node in self.children:
            node.render()

        event('render:post:page:any', self)
        event('render:post:page:path:' + self.path, self)
        if self.id:
            event('render:post:page:id:' + self.id, self)
        for tag in self.tags:
            event('render:post:page:tag:' + tag, self)


class Asset(Node):

    def __init__(self, name, path, parent):
        """create new Asset node"""
        super().__init__(name, path, parent)
        self.key = 'Asset'
        self.url = '/' + self.path

    def ready(self):
        """asset is ready: send event(s)"""
        suffix = splitext(self.path)[1][1:]
        event('generate:post:asset:path:' + self.path, self)
        event('generate:post:asset:extension:' + suffix, self)

    def render(self):
        """render Asset node"""
        suffix = splitext(self.path)[1][1:]
        event('render:pre:asset:path:' + self.path, self)
        event('render:pre:asset:extension:' + suffix, self)
        shutil.copy(join(setting.input, self.path), join(setting.output, self.path))
        event('render:post:asset:path:' + self.path, self)
        event('render:post:asset:extension:' + suffix, self)


def read_page(path):
    """read page from file and return triple (meta, preview, content)"""
    text = read_file(path)
    parts = text.split('\n---\n')
    if len(parts) == 1:
        return ({}, '', parts[0])
    else:
        if len(parts) == 2:
            meta = read_yaml_string(parts[0])
            return (
             meta, '', parts[1])
        meta = read_yaml_string(parts[0])
        return (meta, parts[1], '\n'.join(parts[1:]))