# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/learners/models/model.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 2229 bytes
from typing import Dict

class BaseModel(object):
    """BaseModel"""

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