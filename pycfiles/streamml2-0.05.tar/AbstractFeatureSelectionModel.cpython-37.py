# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\bmccs\Desktop\streamml2\streamml2\streamline\feature_selection\AbstractFeatureSelectionModel.py
# Compiled at: 2019-01-21 12:38:50
# Size of source mod 2**32: 941 bytes


class AbstractFeatureSelectionModel:
    _X = None
    _y = None
    _verbose = None
    _params = None
    _code = None

    def __init__(self, code, X, y, params, verbose):
        self._code = code
        self._X = X
        self._y = y
        self._params = params
        self._verbose = verbose

    def execute(self):
        assert isinstance(self._code, str), 'code must be of type str.'
        assert self._X is not None, "please provide a valid data set, perhaps you didn't construct the model before calling this function."
        assert self._y is not None, "please provide a valid response set, perhaps you didn't construct the model before calling this function."
        assert isinstance(self._params, dict), 'please ensure that params are of type dict.'
        assert isinstance(self._verbose, bool), 'verbose must be of type bool.'
        if self._verbose:
            print('Executing: ' + self._code)