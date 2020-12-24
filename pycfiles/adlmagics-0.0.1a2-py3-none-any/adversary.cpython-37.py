# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/adversaries/adversary.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 2248 bytes
from data_reader.binary_input import Instance
from typing import List, Dict
import copy

class Adversary(object):
    """Adversary"""

    def __init__(self):
        pass

    def attack(self, instances) -> List[Instance]:
        """Transform the set of instances using an adversarial algorithm.

            Args:
                instances (List[Instance]): instances to be transformed.

            Returns:
                transformed instances (List[Instance])

        """
        raise NotImplementedError

    def set_params(self, params: Dict):
        """Set params for the adversary.

        These are user-defined (with existing default values).

            Args:
                params (Dict): set of available params with updated values.

        """
        raise NotImplementedError

    def get_available_params(self) -> Dict:
        """Get the set of adversary-specific params.

            Returns:
                dictionary mapping param names to current values

        """
        raise NotImplementedError

    def set_adversarial_params(self, learner, train_instances):
        """
        Give the adversary knowledge of the initial learner and train instances.

        This standardizes the input to each adversarial function. It is the job
        of any adversaries derived from this class to determine exactly what
        information the adversary is allowed to use.

            Args:
                learner (InitialPredictor): Initial predictive model.
                train_instances (List[Instance]): Instances used by the initial
                learner to create model.
        """
        raise NotImplementedError

    def clone(self):
        """Return a new copy of the adversary with same initial params."""
        new_params = copy.deepcopy(self.get_available_params())
        obj = self.__class__
        new_obj = obj(**new_params)
        return new_obj