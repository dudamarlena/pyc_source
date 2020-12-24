# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parsimony/generators/callable_wrapper.py
# Compiled at: 2014-11-30 19:40:42
# Size of source mod 2**32: 1265 bytes
from parsimony.generators import Generator
from parsimony.configuration import context_name, parsimony_directory
import pickle, os, string

class StoredCallableWrapper(Generator):
    __doc__ = ' Generator for callables using that stores results.\n\n    '

    def __init__(self, key, function, **parameters):
        """The PickledCallableWrapper is a simple way to cache arbitrary function results.  Results are stored in
        the context subdirectory of the parsimony directory.

        :param key: generator key string
        :param function: callable handle
        :param callable_store: store object used to persist. If None is given, the store will be created from configuration
        :param parameters: key-value parameters for the callable function
        """
        self._function = function
        self._param_keys = list(parameters.keys())
        super(StoredCallableWrapper, self).__init__(key, function=function, **parameters)

    def rebuild(self):
        """ Call the callable with parameters to generate the value

        :return: generated value
        """
        params = {key:self.get_parameter(key) for key in self._param_keys}
        return self._function(**params)