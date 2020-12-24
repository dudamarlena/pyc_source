# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\komparse\ast.py
# Compiled at: 2020-03-07 08:14:04
# Size of source mod 2**32: 4169 bytes
import os

class Ast(object):

    def __init__(self, name, value='', id=''):
        self.name = name
        self.value = value
        self.id = id
        self._attrs = {}
        self._parent = None
        self._children = []

    def copy(self):
        """
        Create a shallow copy
        """
        clone = Ast(self.name, self.value, self.id)
        clone._attrs = self._attrs.copy()
        return clone

    def add_child(self, child):
        self._children.append(child)
        child._parent = self

    def add_children_by_name(self, source_ast, name):
        children = source_ast.find_children_by_name(name)
        for child in children:
            child.id = ''
            self.add_child(child)

    def add_children_by_id(self, source_ast, id_):
        children = source_ast.find_children_by_id(id_)
        for child in children:
            child.id = ''
            self.add_child(child)

    def remove_children(self):
        for child in self._children:
            child._parent = None
        else:
            self._children = []

    def get_parent(self):
        return self._parent

    def get_children(self):
        return self._children

    def find_children_by_name(self, name):
        return [child for child in self._children if child.name == name]

    def find_children_by_id(self, id_):
        return [child for child in self._children if child.id == id_]

    def set_attr(self, name, value):
        self._attrs[name] = value

    def get_attr(self, name):
        return self._attrs[name]

    def has_attr(self, name):
        return name in self._attrs

    def to_json(self):
        json = '{{ "name": "{}"'.format(self.name)
        json += ', "value": "{}"'.format(self._json_escape(self.value))
        if self.id:
            json += ', "id": "{}"'.format(self.id)
        if self._attrs:
            attrs_json = ''
            for name, value in self._attrs.items():
                if attrs_json:
                    attrs_json += ', '
                attrs_json += '"{}": "{}"'.format(name, value)
            else:
                json += ', "attributes": {{ {} }}'.format(attrs_json)

        if self._children:
            children_json = ''
            for child in self._children:
                if children_json:
                    children_json += ', '
                children_json += child.to_json()
            else:
                json += ', "children": [{}]'.format(children_json)

        json += ' }'
        return json

    def _json_escape(self, s):
        ret = ''
        for ch in s:
            if ch in ('"', ):
                ch = '\\{}'.format(ch)
            ret += ch
        else:
            return ret

    def to_xml(self, offset=0, delta=2):
        res = '<{}'.format(self.name)
        attrs = self._attrs_to_str()
        if attrs:
            res += ' ' + attrs
        else:
            if not self.value:
                if not self._children:
                    res += '/>'
                    res = self._leftpad(offset, res)
                    return res
            res += '>'
            if self.value:
                res += self.value
            if self._children:
                res = self._leftpad(offset, res) + os.linesep
                for child in self._children:
                    res += child.to_xml(offset + delta, delta) + os.linesep
                else:
                    res += self._leftpad(offset, '</{}>'.format(self.name))

            else:
                res += '</{}>'.format(self.name)
            res = self._leftpad(offset, res)
        return res

    def _attrs_to_str(self):
        if self.id:
            res = 'id="{}"'.format(self.id)
        else:
            res = ''
        for aname in self._attrs:
            if res:
                res += ' '
            res += '{}="{}"'.format(aname, self._attrs[aname])
        else:
            return res

    def _leftpad(self, offset, s):
        return ' ' * offset + s

    def walk(self, visitor):
        if self._children:
            visitor.enter_node(self)
            for child in self._children:
                child.walk(visitor)
            else:
                visitor.exit_node(self)

        else:
            visitor.visit_node(self)