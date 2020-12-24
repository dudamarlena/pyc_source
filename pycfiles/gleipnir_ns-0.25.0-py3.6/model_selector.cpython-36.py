# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gleipnir/pysb_utilities/model_selector.py
# Compiled at: 2019-07-02 15:48:17
# Size of source mod 2**32: 1553 bytes
"""Defines the ModelSelector class, which is a subclass of HypSelector.
"""
from .hyp_selector import HypSelector

class ModelSelector(HypSelector):
    __doc__ = 'A model selector using Nested Sampling-based model selection.\n    ModelSelector is sub-classed from HypSelector.\n\n    Args:\n        models (list of :obj:pysb.Model): A list PySB models to perform model\n        selection on. Filename of the input HypBuilder model csv file.\n\n    Attributes:\n        nested_samplers (list of :obj:): A list containing the Nested Sampler\n            objects. Must call the gen_nested_samplers function build the\n            Sampler instances.\n        selection (pandas.DataFrame): The DataFrame containing the sorted\n            set of models, including their name, log_evidence, and\n            log_evidence_error values. The values are sorted in descending\n            order by the log_evidence values. Only generated after calling\n            the run_nested_sampling function.\n        models\n\n    '

    def __init__(self, models):
        """Inits ModelSelector."""
        self.nested_samplers = None
        self._nested_sample_its = None
        self.selection = None
        self.models = models

    def load_models(self):
        """Does nothing.
        """
        pass

    def append_to_models(self, line):
        """Does nothing.
        """
        pass

    def number_of_models(self):
        """Number of models being tested.

        Returns:
            int: The number of models.

        """
        return len(self.models)