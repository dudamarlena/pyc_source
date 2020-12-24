# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/core/orm/statements.py
# Compiled at: 2013-04-11 17:47:52
import sys
MUTATORS = '__mutators__'

class ClassMutator(object):
    """Class to create DSL statements such as `using_options`.  This is used
    to transform DSL statements in Declarative class attributes.
    The use of these statements is discouraged in any new code, and exists for
    compatibility with Elixir model definitions"""

    def __init__(self, *args, **kwargs):
        class_locals = sys._getframe(1).f_locals
        mutators = class_locals.setdefault(MUTATORS, [])
        mutators.append((self, args, kwargs))

    def process(self, entity_dict, *args, **kwargs):
        """
        Process one mutator.  This method should be overwritten in a subclass
        """
        pass