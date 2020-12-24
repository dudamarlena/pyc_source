# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\modifiers\representation.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 1785 bytes
"""
Module `chatette_qiu.modifiers.representation`
Contains structures that represent the possible modifiers
that could apply to unit declarations or sub-rules.
"""

class BaseModifiersRepr(object):

    def __init__(self, case_generation=False):
        self.casegen = case_generation


class UnitDeclarationModifiersRepr(BaseModifiersRepr):

    def __init__(self, case_generation=False, variation_name=None, argument_name=None):
        super(UnitDeclarationModifiersRepr, self).__init__(case_generation)
        self.variation_name = variation_name
        self.argument_name = argument_name


class WordGroupModifiersRepr(BaseModifiersRepr):

    def __init__(self, case_generation=False, randgen_name=None, percentage_randgen=50):
        super(WordGroupModifiersRepr, self).__init__(case_generation)
        self.randgen_name = randgen_name
        self.percentage_randgen = percentage_randgen


class ChoiceModifiersRepr(BaseModifiersRepr):

    def __init__(self, case_generation=False, randgen=False):
        super(ChoiceModifiersRepr, self).__init__(case_generation)
        self.randgen = randgen


class ReferenceModifiersRepr(BaseModifiersRepr):

    def __init__(self, case_generation=False, randgen_name=None, percentage_randgen=50, variation_name=None, argument_value=None):
        super(ReferenceModifiersRepr, self).__init__(case_generation)
        self.randgen_name = randgen_name
        self.percentage_randgen = percentage_randgen
        self.variation_name = variation_name
        self.argument_value = argument_value