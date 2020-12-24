# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fever/reader/preprocessing.py
# Compiled at: 2019-01-25 08:19:53
# Size of source mod 2**32: 1150 bytes
from typing import List, Tuple
from allennlp.common import Registrable
from overrides import overrides

class FEVERInstanceGenerator(Registrable):

    def generate_instances(self, reader, evidence: List[List[Tuple[(int, str, int)]]], claim: str):
        raise NotImplemented('This preprocessing function should be implemented')


@FEVERInstanceGenerator.register('concatenate')
class ConcatenateEvidence(FEVERInstanceGenerator):

    @staticmethod
    def _flatten(l):
        return [item for sublist in l for item in sublist]

    @overrides
    def generate_instances(self, reader, evidence: List[List[Tuple[(int, str, int)]]], claim: str):
        evidence_text = [[reader.get_doc_line(item[1], item[2]) for item in group] for group in evidence]
        flat_evidence_text = self._flatten(evidence_text)
        evidence_dict = dict()
        for item in flat_evidence_text:
            evidence_dict[item] = 1

        evidence = ' '.join(evidence_dict.keys())
        return [
         {'evidence':evidence, 
          'claim':claim,  'evidence_group':None}]