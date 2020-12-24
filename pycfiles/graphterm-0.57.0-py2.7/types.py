# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/svgwrite/data/types.py
# Compiled at: 2012-08-15 03:48:07


class SVGAttribute(object):

    def __init__(self, name, anim, types, const):
        self.name = name
        self._anim = anim
        self._types = types
        self._const = const

    def get_anim(self, elementname='*'):
        return self._anim

    def get_types(self, elementname='*'):
        return self._types

    def get_const(self, elementname='*'):
        return self._const


class SVGMultiAttribute(object):

    def __init__(self, attributes):
        self.name = None
        self._attributes = {}
        firstkey = None
        for names, attribute in attributes.items():
            for name in names.split():
                name = name.strip()
                self._attributes[name] = attribute
                if not self.name:
                    self.name = attribute.name
                elif self.name != attribute.name:
                    raise ValueError('Different attribute-names for SVGMultiAttribute (%s != %s).' % (
                     self.name, attribute.name))
                if not firstkey:
                    firstkey = name

        if '*' not in self._attributes:
            self._attributes['*'] = self._attributes[firstkey]
        return

    def get_attribute(self, elementname):
        if elementname in self._attributes:
            return self._attributes[elementname]
        else:
            return self._attributes['*']

    def get_anim(self, elementname='*'):
        attribute = self.get_attribute(elementname)
        return attribute.get_anim()

    def get_types(self, elementname='*'):
        attribute = self.get_attribute(elementname)
        return attribute.get_types()

    def get_const(self, elementname='*'):
        attribute = self.get_attribute(elementname)
        return attribute.get_const()


class SVGElement(object):

    def __init__(self, name, attributes, properties, children):
        self.name = name
        s = set(attributes)
        s.update(properties)
        self.valid_attributes = frozenset(s)
        self.valid_children = frozenset(children)