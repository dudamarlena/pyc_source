# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\billingtonm\dropbox\code\pydiagrams\build\lib\pydiagrams\Component.py
# Compiled at: 2019-10-20 22:53:52
# Size of source mod 2**32: 5883 bytes
from contextlib import contextmanager
import pydiagrams.Diagram as Diagram
from pydiagrams.helpers.PUML import Helper
from .helpers.constants import *
Component = 'Component'
Interface = 'Interface'
Cloud = 'Cloud'
Database = 'Database'
Folder = 'Folder'
Frame = 'Frame'
Node = 'Node'
Package = 'Package'
Rectangle = 'Rectangle'

class ComponentDiagramItem(Diagram.Item):
    __doc__ = ' Base class for all Items in a component Diagram '

    def __init__(self, label, shape, **attrs):
        (Diagram.Item.__init__)(self, label, **attrs)
        self.attrs['shape'] = shape

    def __hash__(self):
        return hash(self.label)

    def __rshift__(self, i2):
        """ Override the >> operator to mean to add an edge between this item and the i2 """
        return self.link_edge(i2, 'vertical')

    def __xor__(self, i2):
        """ Override the ^ operator to mean to add an 'up' edge """
        return self.link_edge(i2, 'up')

    def __or__(self, i2):
        """ Override the ^ operator to mean to add an 'up' edge """
        return self.link_edge(i2, 'down')

    def __ge_(self, i2):
        """ Override the >= operator to mean to add an 'right' edge """
        return self.link_edge(i2, 'right')

    def __le__(self, i2):
        """ Override the <= operator to mean to add an 'left' edge """
        return self.link_edge(i2, 'left')

    def __sub__(self, i2):
        """ Override the - operator to add a horizontal line """
        return self.link_edge(i2, 'hline')

    def __eq__(self, i2):
        return self.link_edge(i2, 'vline')

    def __irshift__(self, i2):
        return self.link_edge(i2, 'vdotted')


class ComponentDiagram(Diagram.DiagramBase):

    def __init__(self, helper, filename=None, **attrs):
        (Diagram.DiagramBase.__init__)(self, helper, filename, **attrs)

    def Group(self, shape, label, **attrs):
        g = ComponentSubDiagram(parent=self, id=None, shape=shape, label=label, **attrs)
        self.collection.add_item(g)
        return g

    def add_new_item(self, shape, label, **kwargs):
        i = ComponentDiagramItem(label, shape, **kwargs)
        return self.collection.add_item(i)

    def Component(self, label, **attrs):
        return (self.add_new_item)(Component, label, **attrs)

    def Interface(self, label, **attrs):
        return (self.add_new_item)(Interface, label, **attrs)

    def Actor(self, label, **attrs):
        return (self.add_new_item)('actor', label, **attrs)

    def Cloud(self, label=None, **attrs):
        return (self.Group)(Cloud, label, **attrs)

    def Database(self, label=None, **attrs):
        return (self.Group)(Database, label, **attrs)

    def Folder(self, label=None, **attrs):
        return (self.Group)(Folder, label, **attrs)

    def Frame(self, label=None, **attrs):
        return (self.Group)(Frame, label, **attrs)

    def Node(self, label=None, **attrs):
        return (self.Group)(Node, label, **attrs)

    def Package(self, label=None, **attrs):
        return (self.Group)(Package, label, **attrs)

    def Rectangle(self, label=None, **attrs):
        return (self.Group)(Rectangle, label, **attrs)


class ComponentSubDiagram(ComponentDiagram, Diagram.Item):

    def __init__(self, parent, id, shape, label, **attrs):
        (ComponentDiagram.__init__)(self, helper=parent.helper, **attrs)
        (Diagram.Item.__init__)(self, label, **attrs)
        self.attrs['shape'] = shape
        self.parent = parent
        self.id = id
        self.level = self.parent.level + 1
        self.node_attrs = parent.node_attrs.copy()
        self.edge_attrs = parent.edge_attrs.copy()
        self.is_group = False

    def __str__(self):
        if self.is_group:
            a = (self.helper.startSubdiagram)((self.id), (self.label), **self.attrs)
            a += '\n'.join([str(v) for v in list(self.collection.values())])
            a += (self.helper.endSubdiagram)((self.id), (self.label), **self.attrs)
            return a
        return Diagram.Item.__str__(self)

    def __enter__(self):
        self.is_group = True
        return self

    def __exit__(*args):
        pass


class ComponentContextPUML(Diagram.Context):

    def __init__(self, filename=None):
        print(('Generating!:', filename))
        self.diagram = ComponentDiagram(Helper, filename)


class ComponentContext(Diagram.Context):

    def __init__(self, helper, filename=None):
        print(f"Generating-: {filename}")
        self.diagram = ComponentDiagram(helper, filename)