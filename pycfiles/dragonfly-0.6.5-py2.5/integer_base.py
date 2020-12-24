# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\language\base\integer_base.py
# Compiled at: 2009-03-23 04:13:41
"""
This file implements base classes for structured integer grammar
elements.

"""
from dragonfly.grammar.elements import Alternative, Sequence, Optional, Compound, ListRef
from dragonfly.grammar.list import List

class IntegerBase(Alternative):
    _builders = ()

    def __init__(self, name=None, min=None, max=None):
        self._min = min
        self._max = max
        children = self._build_children(min, max)
        Alternative.__init__(self, children, name=name)

    def __str__(self):
        arguments = []
        if self.name is not None:
            arguments = [
             '%r' % self.name]
        if self._min is not None or self._max is not None:
            arguments.append('%s' % self._min)
            arguments.append('%s' % self._max)
        return '%s(%s)' % (self.__class__.__name__, (',').join(arguments))

    def _build_children(self, min, max):
        children = [ c.build_element(min, max) for c in self._builders
                   ]
        return [ c for c in children if c ]


class IntBuilderBase(object):

    def __init__(self):
        pass

    def build_element(self, min, max):
        raise NotImplementedError('Call to virtual method build_element() in base class IntBuilderBase')


class MapIntBuilder(IntBuilderBase):

    def __init__(self, mapping):
        self._mapping = mapping

    def build_element(self, min, max):
        elements = [ (spec, value) for (spec, value) in self._mapping.iteritems() if min <= value < max
                   ]
        if len(elements) > 1:
            children = [ Compound(spec=spec, value=value) for (spec, value) in elements ]
            return Alternative(children)
        elif len(elements) == 1:
            return Compound(spec=elements[0][0], value=elements[0][1])
        else:
            return
        return


class CollectionIntBuilder(IntBuilderBase):

    def __init__(self, spec, set):
        self._spec = spec
        self._set = set

    def build_element(self, min, max):
        child = self._build_range_set(self._set, min, max)
        if not child:
            return
        child.name = 'element'
        element = Collection(self._spec, child)
        return element

    def _build_range_set(self, set, min, max):
        children = [ c.build_element(min, max) for c in set ]
        children = [ c for c in children if c ]
        if not children:
            return
        if len(children) == 1:
            return children[0]
        else:
            return Alternative(children)
        return


class MagnitudeIntBuilder(IntBuilderBase):

    def __init__(self, factor, spec, multipliers, remainders):
        self._factor = factor
        self._spec = spec
        self._multipliers = multipliers
        self._remainders = remainders

    def build_element(self, min, max):
        if min >= max:
            return
        first_multiplier = min / self._factor
        last_multiplier = (max - 1) / self._factor + 1
        first_remainder = min % self._factor
        last_remainder = max % self._factor
        if last_remainder == 0:
            last_remainder = self._factor
        if first_multiplier == last_multiplier - 1:
            return self._build_range(first_multiplier, last_multiplier, first_remainder, last_remainder)
        children = []
        if first_remainder > 0:
            c = self._build_range(first_multiplier, first_multiplier + 1, first_remainder, self._factor)
            if c:
                children.append(c)
            first_multiplier += 1
        if last_remainder > 0:
            c = self._build_range(last_multiplier - 1, last_multiplier, 0, last_remainder)
            if c:
                children.append(c)
            last_multiplier -= 1
        if first_multiplier < last_multiplier:
            c = self._build_range(first_multiplier, last_multiplier, 0, self._factor)
            if c:
                children.append(c)
        if len(children) == 0:
            return
        elif len(children) == 1:
            return children[0]
        else:
            return Alternative(children)
        return

    def _build_range(self, first_multiplier, last_multiplier, first_remainder, last_remainder):
        multipliers = self._build_range_set(self._multipliers, first_multiplier, last_multiplier)
        if not multipliers:
            return
        remainders = self._build_range_set(self._remainders, first_remainder, last_remainder)
        if not remainders:
            l = List('_MagnitudeIntBuilder_empty')
            remainders = ListRef('_MagnitudeIntBuilder_emptyref', l)
        multipliers.name = 'multiplier'
        remainders.name = 'remainder'
        return Magnitude(self._factor, self._spec, multipliers, remainders)

    def _build_range_set(self, set, min, max):
        children = [ c.build_element(min, max) for c in set ]
        children = [ c for c in children if c ]
        if not children:
            return
        if len(children) == 1:
            return children[0]
        else:
            return Alternative(children)
        return


class Collection(Compound):
    _element_name = 'element'
    _default_value = None

    def __init__(self, spec, element, name=None):
        self._element = element
        Compound.__init__(self, spec, extras=[element], name=name)

    def value(self, node):
        child_node = node.get_child_by_name(self._element_name, shallow=True)
        if child_node:
            return child_node.value()
        else:
            return self._default_value


class Magnitude(Compound):
    _mul_default = 1
    _rem_default = 0

    def __init__(self, factor, spec, multiplier, remainder, name=None):
        self._factor = factor
        self._mul = multiplier
        self._rem = remainder
        Compound.__init__(self, spec, extras=[multiplier, remainder], name=name)

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, self._factor)

    def value(self, node):
        mul_node = node.get_child_by_name(self._mul.name, shallow=True)
        rem_node = node.get_child_by_name(self._rem.name, shallow=True)
        if mul_node:
            multiplier = mul_node.value()
        else:
            multiplier = self._mul_default
        if rem_node:
            remainder = rem_node.value()
        else:
            remainder = self._rem_default
        return multiplier * self._factor + remainder