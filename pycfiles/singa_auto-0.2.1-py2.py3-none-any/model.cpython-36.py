# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nailixing/PyProjects/nusdb_rafiki/singa_auto/model/model.py
# Compiled at: 2020-04-24 21:27:49
# Size of source mod 2**32: 6203 bytes
import abc, numpy as np
from typing import Union, Dict, Optional, Any, List
from .knob import BaseKnob
KnobConfig = Dict[(str, BaseKnob)]
Knobs = Dict[(str, Any)]
Params = Dict[(str, Union[(str, int, float, np.ndarray)])]

class BaseModel(abc.ABC):
    __doc__ = "\n    SINGA-Auto's base model class that SINGA-Auto models must extend.\n\n    SINGA-Auto models must implement all abstract methods below, according to the specification of its associated task (see :ref:`tasks`).\n    They configure how this model template will be trained, evaluated, tuned, serialized and served on SINGA-Auto.\n\n    In the model's ``__init__`` method, call ``super().__init__(**knobs)`` as the first line,\n    followed by the model's initialization logic. The model should be initialize itself with ``knobs``,\n    a set of generated knob values for the created model instance.\n\n    These knob values are chosen by SINGA-Auto based on the model's knob configuration (defined in :meth:`singa_auto.model.BaseModel.get_knob_config`).\n\n    For example:\n\n    ::\n\n        def __init__(self, **knobs):\n            super().__init__(**knobs)\n            self.__dict__.update(knobs)\n            ...\n            self._build_model(self.knob1, self.knob2)\n\n    :param knobs: Dictionary mapping knob names to knob values\n    :type knobs: :obj:`singa_auto.model.Knobs`\n    "

    def __init__(self, **knobs: Knobs):
        pass

    @abc.abstractstaticmethod
    def get_knob_config() -> KnobConfig:
        """
        Return a dictionary that defines the search space for this model template's knobs
        (i.e. knobs' names, their types & their ranges).

        Over the course of training, your model will be initialized with different values of knobs within this search space
        to maximize this model’s performance.

        Refer to :ref:`model-tuning` to understand more about how this works.

        :returns: Dictionary mapping knob names to knob specifications
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def train(self, dataset_path: str, shared_params: Optional[Params]=None, **train_args):
        """
        Train this model instance with the given traing dataset and initialized knob values.
        Additional keyword arguments could be passed depending on the task's specification.

        Additionally, trained parameters shared from previous trials could be passed,
        as part of the ``SHARE_PARAMS`` policy (see :ref:`model-policies`).

        Subsequently, the model is considered *trained*.

        :param dataset_path: File path of the train dataset file in the *local filesystem*, in a format specified by the task
        :param shared_params: Dictionary mapping parameter names to values, as produced by your model's :meth:`singa_auto.model.BaseModel.dump_parameters`.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def evaluate(self, dataset_path: str) -> float:
        """
        Evaluate this model instance with the given validation dataset after training.

        This will be called only when model is *trained*.

        :param dataset_path: File path of the validation dataset file in the *local filesystem*, in a format specified by the task
        :returns: A score associated with the validation performance for the trained model instance, the higher the better e.g. classification accuracy.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def predict(self, queries: List[Any]) -> List[Any]:
        """
        Make predictions on a batch of queries after training.

        This will be called only when model is *trained*.

        :param queries: List of queries, where a query is in the format specified by the task
        :returns: List of predictions, in an order corresponding to the queries, where a prediction is in the format specified by the task
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def dump_parameters(self) -> Params:
        """
        Returns a dictionary of model parameters that *fully define the trained state of the model*.
        This dictionary must conform to the format :obj:`singa_auto.model.Params`.
        This will be used to save the trained model in SINGA-Auto.

        Additionally, trained parameters produced by this method could be shared with future trials, as
        part of the ``SHARE_PARAMS`` policy (see :ref:`model-policies`).

        This will be called only when model is *trained*.

        :returns: Dictionary mapping parameter names to values
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def load_parameters(self, params: Params):
        """
        Loads this model instance with previously trained model parameters produced by your model's :meth:`singa_auto.model.BaseModel.dump_parameters`.
        *This model instance's initialized knob values will match those during training*.

        Subsequently, the model is considered *trained*.
        """
        raise NotImplementedError()

    def destroy(self):
        """
        Destroy this model instance, freeing any resources held by this model instance.
        No other instance methods will be called subsequently.
        """
        pass

    @staticmethod
    def teardown():
        """
        Runs class-wide teardown logic (e.g. close a training session shared across trials).
        """
        pass