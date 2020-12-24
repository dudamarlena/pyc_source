# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/pygenprop/functional_element.py
# Compiled at: 2019-04-06 18:17:06
# Size of source mod 2**32: 1542 bytes
"""
Created by: Lee Bergstrand (2017)

Description: The functional element class.
"""
from pygenprop.step import Step

class FunctionalElement(object):
    __doc__ = 'A functional element (enzyme, structural component or sub-genome property) that can carry out a step.'

    def __init__(self, identifier, name, evidence: list=None, required=False, parent: Step=None):
        """
        Creates a new FunctionalElement object.

        :param identifier: The identifier of the FunctionalElement.
        :param name: The name of the FunctionalElement.
        :param evidence: A list of Evidence objects supporting this FunctionalElement.
        :param required: Is this a required FunctionalElement for this functional_element?
        """
        if evidence is None:
            evidence = []
        else:
            for current_evidence in evidence:
                current_evidence.parent = self

        if required is None:
            required = False
        if name is None:
            name = identifier
        self.id = identifier
        self.name = name
        self.evidence = evidence
        self.required = required
        self.parent = parent

    def __repr__(self):
        repr_data = [
         'ID: ' + str(self.id),
         'Name: ' + str(self.name),
         'Evidences: ' + str(self.evidence),
         'Required: ' + str(self.required)]
        return '(' + ', '.join(repr_data) + ')'