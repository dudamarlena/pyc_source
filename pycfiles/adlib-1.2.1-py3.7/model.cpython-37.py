# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/learners/models/model.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 2229 bytes
from typing import Dict

class BaseModel(object):
    __doc__ = 'Abstract base class for learner model\n\n    Defines necessary operations for the underlying\n    learner model; training, prediction, classification\n    probabilities, and decision function results. In order\n    for an initial or improved learner to use a future-defined\n    model, the model must include these operations\n\n    '

    def train(self, instances):
        """Train on the set of training instances.

        Returns:
            None.

        """
        raise NotImplementedError

    def predict(self, instances):
        """Predict classification labels for the set of instances.

        Returns:
            label classifications (List(int))

        """
        raise NotImplementedError

    def predict_proba(self, instances):
        """Use the model to determine probability of adversarial classification.

        Returns:
            probability of adversarial classification (List(int))

        """
        raise NotImplementedError

    def predict_log_proba(self, instances):
        """Use the model to determine probability of adversarial classification.

        Returns:
            probability of adversarial classification (List(int))

        """
        raise NotImplementedError

    def decision_function_(self, instances):
        """Use the model to determine the decision function for each instance.

        Returns:
            decision values (List(int))

        """
        raise NotImplementedError

    def set_params(self, params: Dict):
        """Set params for the model.

        Args:
            params (Dict): set of available params with updated values

        """
        raise NotImplementedError

    def get_available_params(self) -> Dict:
        """Get the set of params defined in the model usage.

        Returns:
            dictionary mapping param names to current values

        """
        raise NotImplementedError

    def get_alg(self):
        """Return the underlying model algorithm.

        Returns:
            algorithm used to train and test instances

        """
        raise NotImplementedError