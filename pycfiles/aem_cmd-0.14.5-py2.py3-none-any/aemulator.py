# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Aemulator/aemulator.py
# Compiled at: 2018-12-10 13:02:09
__doc__ = '\nContains the Aemulator abtract base class that all other emulators in this project will\ncomply with.\n'
__author__ = 'Sean McLaughlin'
__email__ = 'swmclau2@stanford.edu'
from abc import ABCMeta, abstractmethod

class Aemulator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def load_data(self, filename):
        """
        Load training data directly from file, and attach it to this object.
        :param filename:
            Location of the training data. May be a single file, or a directory of files.
        :return:
            None
        """
        pass

    @abstractmethod
    def build_emulator(self, hyperparams=None):
        """
        Build the emulator directly from loaded training data.

        Optionally provide hyperparameters, if something other than the default is preferred.
        :param hyperparams:
            A dictionary of hyperparameters for the emulator. Default is None.
        :return:
            None
        """
        pass

    @abstractmethod
    def train_emulator(self):
        """
        Optimize the hyperparmeters of a built emulator against training data.
        :return:
            None
        """
        pass

    @abstractmethod
    def cache_emulator(self, filename):
        """
        Cache the emulator to a file for easier re-loadig. 
        :param filename:
            The filename where the trained emulator will be cached.
        :return:
            None
        """
        pass

    @abstractmethod
    def load_emulator(self, filename):
        """
        Load an emulator directly from file, pre-trained.
        :param filename:
            The filename where the trained emulator is located, in a format compatible with
            this object.
        :return:
            None
        """
        pass

    @abstractmethod
    def predict(self, params):
        """
        Use the emulator to make a prediction at a point in parameter space.
        :param params:
            A dictionary of parameters, where the key is the parameter name and
            value is its value.
        :return:
            pred, the emulator prediction at params. Will be a float or numpy array,
            depending on the quantity being emulated.
        """
        pass