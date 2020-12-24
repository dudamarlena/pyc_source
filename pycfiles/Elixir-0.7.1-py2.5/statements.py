# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/elixir/statements.py
# Compiled at: 2009-10-02 06:19:50
import sys
MUTATORS = '__elixir_mutators__'

class ClassMutator(object):
    """
    DSL-style syntax

    A ``ClassMutator`` object represents a DSL term.
    """

    def __init__(self, handler):
        """
        Create a new ClassMutator, using the `handler` callable to process it
        when the time will come.
        """
        self.handler = handler

    def __call__(self, *args, **kwargs):
        class_locals = sys._getframe(1).f_locals
        mutators = class_locals.setdefault(MUTATORS, [])
        mutators.append((self, args, kwargs))

    def process(self, entity, *args, **kwargs):
        """
        Process one mutator. This version simply calls the handler callable,
        but another mutator (sub)class could do more processing.
        """
        self.handler(entity, *args, **kwargs)


def process_mutators(entity):
    """
    Apply all mutators of the given entity. That is, loop over all mutators
    in the class's mutator list and process them.
    """
    mutators = entity.__dict__.get(MUTATORS, [])
    for (mutator, args, kwargs) in mutators:
        mutator.process(entity, *args, **kwargs)


class Statement(ClassMutator):

    def process(self, entity, *args, **kwargs):
        builder = self.handler(entity, *args, **kwargs)
        entity._descriptor.builders.append(builder)


class PropertyStatement(ClassMutator):

    def process(self, entity, name, *args, **kwargs):
        prop = self.handler(*args, **kwargs)
        prop.attach(entity, name)