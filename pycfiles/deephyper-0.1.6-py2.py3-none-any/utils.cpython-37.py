# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/deepq/utils.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1938 bytes
from deephyper.search.nas.baselines.common.input import observation_input
from deephyper.search.nas.baselines.common.tf_util import adjust_shape

class TfInput(object):

    def __init__(self, name='(unnamed)'):
        """Generalized Tensorflow placeholder. The main differences are:
            - possibly uses multiple placeholders internally and returns multiple values
            - can apply light postprocessing to the value feed to placeholder.
        """
        self.name = name

    def get(self):
        """Return the tf variable(s) representing the possibly postprocessed value
        of placeholder(s).
        """
        raise NotImplementedError

    def make_feed_dict(self, data):
        """Given data input it to the placeholder(s)."""
        raise NotImplementedError


class PlaceholderTfInput(TfInput):

    def __init__(self, placeholder):
        super().__init__(placeholder.name)
        self._placeholder = placeholder

    def get(self):
        return self._placeholder

    def make_feed_dict(self, data):
        return {self._placeholder: adjust_shape(self._placeholder, data)}


class ObservationInput(PlaceholderTfInput):

    def __init__(self, observation_space, name=None):
        """Creates an input placeholder tailored to a specific observation space

        Parameters
        ----------

        observation_space:
                observation space of the environment. Should be one of the gym.spaces types
        name: str
                tensorflow name of the underlying placeholder
        """
        inpt, self.processed_inpt = observation_input(observation_space,
          name=name)
        super().__init__(inpt)

    def get(self):
        return self.processed_inpt