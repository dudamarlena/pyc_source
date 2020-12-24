# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\grammar\elements_compound.py
# Compiled at: 2009-04-07 12:11:15
"""
    This file implements the Compound grammar element class for
    creating grammar element structures based on a simple text format.
"""
import string, dragonfly.grammar.elements_basic as elements_, dragonfly.parser as parser_, dragonfly.log as log_

class _Stuff(parser_.Sequence):

    def __init__(self):
        self._single = None
        return

    def initialize(self):
        self._single = _Single()
        self._single.initialize()
        repetition = parser_.Repetition(self._single)
        elements = (
         repetition,
         parser_.Repetition(parser_.Sequence((
          parser_.String('|'),
          repetition)), min=0))
        parser_.Sequence.__init__(self, elements)

    def set_elements(self, identifiers):
        self._single.set_elements(identifiers)

    def set_actions(self, identifiers):
        self._single.set_actions(identifiers)

    def value(self, node):
        repetitions = [
         node.children[0].value()]
        for repetition in node.children[1].children:
            repetitions.append(repetition.children[1].value())

        alternatives = []
        for repetition in repetitions:
            if len(repetition) == 1:
                alternatives.append(repetition[0])
            else:
                element = elements_.Sequence(repetition)
                alternatives.append(element)

        if len(alternatives) == 1:
            return alternatives[0]
        else:
            return elements_.Alternative(alternatives)


stuff = _Stuff()

class _Single(parser_.Sequence):

    def __init__(self):
        pass

    def initialize(self):
        self._element_identifier = _ElementRef()
        self._action_identifier = _ActionRef()
        alternatives = parser_.Alternative((
         _Literal(),
         _Optional(),
         _Group(),
         self._element_identifier))
        elements = [
         parser_.Whitespace(optional=True),
         alternatives,
         parser_.Optional(parser_.Sequence((
          parser_.Whitespace(optional=True),
          self._action_identifier))),
         parser_.Whitespace(optional=True)]
        parser_.Sequence.__init__(self, elements)

    def set_elements(self, identifiers):
        self._element_identifier.set_identifiers(identifiers)

    def set_actions(self, identifiers):
        self._action_identifier.set_identifiers(identifiers)

    def value(self, node):
        alternative = node.children[1]
        element = alternative.children[0].value()
        optional = node.children[2]
        if optional.children:
            action = optional.children[0].children[1].value()
            element.add_action(action)
        return element


class _ElementRef(parser_.Sequence):

    def __init__(self):
        characters = string.letters + string.digits + '_'
        name = parser_.CharacterSeries(characters)
        elements = (parser_.String('<'), name, parser_.String('>'))
        parser_.Sequence.__init__(self, elements)
        self._identifiers = None
        return

    def set_identifiers(self, identifiers):
        self._identifiers = identifiers

    def value(self, node):
        name = node.children[1].value()
        try:
            return self._identifiers[name]
        except KeyError:
            root = node
            while root.parent:
                root = root.parent

            s = 'Unknown reference name %r in %r' % (node.data, root.data)
            raise Exception(s)


class _ActionRef(parser_.Sequence):

    def __init__(self):
        characters = string.letters + string.digits + '_'
        name = parser_.CharacterSeries(characters)
        elements = (parser_.String('{'), name, parser_.String('}'))
        parser_.Sequence.__init__(self, elements)
        self._identifiers = None
        return

    def set_identifiers(self, identifiers):
        self._identifiers = identifiers

    def value(self, node):
        name = node.children[1].value()
        try:
            return self._identifiers[name]
        except KeyError:
            root = node
            while root.parent:
                root = root.parent

            s = 'Unknown reference name %r in %r' % (node.data, root.data)
            raise Exception(s)


class _Literal(parser_.Sequence):

    def __init__(self):
        characters = string.letters + string.digits + "_-.'"
        word = parser_.CharacterSeries(characters)
        whitespace = parser_.Whitespace()
        elements = (
         word,
         parser_.Repetition(parser_.Sequence((whitespace, word)), min=0))
        parser_.Sequence.__init__(self, elements)

    def value(self, node):
        return elements_.Literal(node.match())


class _Optional(parser_.Sequence):

    def __init__(self):
        elements = (
         parser_.String('['), stuff, parser_.String(']'))
        parser_.Sequence.__init__(self, elements)

    def value(self, node):
        child = node.children[1].value()
        return elements_.Optional(child)


class _Group(parser_.Sequence):

    def __init__(self):
        elements = (
         parser_.String('('), stuff, parser_.String(')'))
        parser_.Sequence.__init__(self, elements)

    def value(self, node):
        child = node.children[1].value()
        return child


stuff.initialize()

class Compound(elements_.Alternative):
    _log = log_.get_log('compound.parse')
    _parser = parser_.Parser(stuff, _log)

    def __init__(self, spec, extras=None, actions=None, name=None, value=None, value_func=None, elements=None):
        self._spec = spec
        self._value = value
        self._value_func = value_func
        if extras is None:
            extras = {}
        if actions is None:
            actions = {}
        if elements is None:
            elements = {}
        if isinstance(extras, (tuple, list)):
            mapping = {}
            for element in extras:
                if not isinstance(element, elements_.ElementBase):
                    self._log.error('Invalid extras item: %s' % element)
                    raise TypeError('Invalid extras item: %s' % element)
                if not element.name:
                    self._log.error('Extras item does not have a name: %s' % element)
                    raise TypeError('Extras item does not have a name: %s' % element)
                if element.name in mapping:
                    self._log.warning('Multiple extras items with the same name: %s' % element)
                mapping[element.name] = element

            extras = mapping
        elif not isinstance(extras, dict):
            self._log.error('Invalid extras argument: %s' % extras)
            raise TypeError('Invalid extras argument: %s' % extras)
        if extras and elements:
            extras = dict(extras)
            extras.update(elements)
        elif elements:
            extras = elements
        self._extras = extras
        stuff.set_elements(extras)
        stuff.set_actions(actions)
        element = self._parser.parse(spec)
        if not element:
            self._log.error('Invalid compound spec: %r' % spec)
            raise SyntaxError('Invalid compound spec: %r' % spec)
        elements_.Alternative.__init__(self, (element,), name=name)
        return

    def __str__(self):
        arguments = ['%r' % self._spec]
        if self.name:
            arguments.append('name=%r' % self.name)
        arguments = (', ').join(arguments)
        return '%s(%s)' % (self.__class__.__name__, arguments)

    def value(self, node):
        if self._value_func is not None:
            extras = {}
            for (name, element) in self._extras.iteritems():
                extra_node = node.get_child_by_name(name, shallow=True)
                if not extra_node:
                    continue
                extras[name] = extra_node.value()

            try:
                value = self._value_func(node, extras)
            except Exception, e:
                self._log.warning('Exception from value_func: %s' % e)
                raise
            else:
                return value
        elif self._value is not None:
            return self._value
        else:
            elements_.Alternative.value(self, node)
        return


class Choice(elements_.Alternative):

    def __init__(self, name, choices, extras=None):
        assert isinstance(name, str) or name is None
        assert isinstance(choices, dict)
        for (k, v) in choices.iteritems():
            assert isinstance(k, str)

        self._choices = choices
        self._extras = extras
        children = []
        for (k, v) in choices.iteritems():
            child = Compound(spec=k, value=v, extras=extras)
            children.append(child)

        elements_.Alternative.__init__(self, children=children, name=name)
        return