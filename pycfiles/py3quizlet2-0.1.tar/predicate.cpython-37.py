# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/hedwig/core/predicate.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 2516 bytes
__doc__ = '\nPredicate-related classes.\n\n@author: anze.vavpetic@ijs.si\n'

class Predicate:
    """Predicate"""
    i = -1

    def __init__(self, label, kb, producer_pred):
        self.label = label
        self.kb = kb
        self.producer_predicate = producer_pred
        if self.producer_predicate:
            producer_pred.consumer_predicate = self
        self.consumer_predicate = None

    @staticmethod
    def _avar():
        """
        Anonymous var name generator.
        """
        Predicate.i = Predicate.i + 1
        return 'X%d' % Predicate.i


class UnaryPredicate(Predicate):
    """UnaryPredicate"""

    def __init__(self, label, members, kb, producer_pred=None, custom_var_name=None, negated=False):
        Predicate.__init__(self, label, kb, producer_pred)
        if not producer_pred:
            if not custom_var_name:
                self.input_var = Predicate._avar()
            else:
                self.input_var = custom_var_name
        else:
            self.input_var = producer_pred.output_var
        self.output_var = self.input_var
        self.negated = negated
        self.domain = {self.input_var: members}


class BinaryPredicate(Predicate):
    """BinaryPredicate"""

    def __init__(self, label, pairs, kb, producer_pred=None):
        """
        The predicate's name and the tuples satisfying it.
        """
        Predicate.__init__(self, label, kb, producer_pred)
        if not producer_pred:
            self.input_var = Predicate._avar()
        else:
            self.input_var = producer_pred.output_var
        self.output_var = Predicate._avar()
        if producer_pred:
            prod_out_var = self.producer_predicate.output_var
            potential_inputs = self.producer_predicate.domain[prod_out_var]
            inputs = potential_inputs & kb.get_domains(label)[0]
            outputs = kb.get_empty_domain()
            for el1 in kb.bits_to_indices(inputs):
                outputs |= pairs[el1]

        else:
            inputs, outputs = kb.get_domains(label)
        self.domain = {self.input_var: inputs, self.output_var: outputs}