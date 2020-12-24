# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/optimization/hyperparameters.py
# Compiled at: 2019-09-11 10:06:18
# Size of source mod 2**32: 10138 bytes
import numpy as np
from photonai.photonlogger import Logger

class PhotonHyperparam:
    pass


class Categorical(PhotonHyperparam):
    __doc__ = "\n      Class for defining a  definite list of hyperparameter values.\n      Can be used for categorical values, but also for numbers.\n\n      Parameters\n      ----------\n      * 'values' [list]:\n         definite list of hyperparameter values\n\n    "

    def __init__(self, values: list):
        self.values = values

    def __getitem__(self, item):
        return self.values.__getitem__(item)

    def index(self, obj):
        return self.values.index(obj)


class BooleanSwitch(PhotonHyperparam):
    __doc__ = "\n      Class for defining a boolean hyperparameter, when both options should be tested in hyperparameter optimization.\n\n      Parameters\n      ----------\n      * 'values' [bool]:\n         will return both True, and False\n\n    "

    def __init__(self):
        self.values = [
         True, False]


class NumberRange(PhotonHyperparam):
    __doc__ = '\n      Class for easily creating a range of numbers to be tested in hyperparameter optimization.\n\n      Parameters\n      ----------\n      * \'start\' [number]:\n         The start value for generating the number interval.\n         The resulting interval includes the value, default is 0.\n\n      * \'stop\' [number]:\n         The stop value for generating the number interval.\n\n         - if range_type == "range":\n           the end value is not included in the interval (see documentation of numpy.arange).\n         - if range_type == "linspace"\n           the end value is included in the interval,\n           unless endpoint is set to False (see documentation of numpy.linspace).\n        - if range_type == "logspace"\n           the end value is included in the interval,\n           unless endpoint is set to False (see documentation of numpy.logspace).\n        - if range_type == "geomspace"\n           the end value is included in the interval,\n           unless endpoint is set to False (see documentation of numpy.logspace).\n\n      * \'range_type\' [str]:\n         Which method to use for generating the number interval.\n         Possible options:\n\n         - "range": numpy.arange is used to generate a list of values separated by the same step width.\n         - "linspace": numpy.linspace is used to generate a certain number of values between start and stop.\n         - "logspace": numpy.logspace is used to generate a logarithmically distributed range of a certain length.\n         - "geomspace": numpy.geomspace is used to generate numbers spaced evenly on a log scale (geometric progression)\n\n      * \'num_type\' [numpy.dtype]:\n         The specific type specification for the interval\'s numbers.\n\n         For the inheriting class IntegerRange it is set to np.int32.\n         For the inheriting class FloatRange it is set to np.float32.\n\n      * \'step\' [number, default=None, optional]:\n        if range_type == \'range\', the spacing between values.\n\n      * \'num\' [int, default=None, optional]:\n        if range_type == \'linspace\' or range_type == \'logspace\' or range_type == \'geomspace\',\n        the number of samples to generate.\n\n      * \'kwargs\' [dict, optional]:\n        Further parameters that should be passed to the numpy function chosen with range_type.\n    '

    def __init__(self, start, stop, range_type, step=None, num=None, num_type=np.int64, **kwargs):
        self.start = start
        self.stop = stop
        self._range_type = None
        self.range_type = range_type
        self.range_params = kwargs
        self.num_type = num_type
        self.values = None
        self.step = step
        self.num = num

    def transform(self):
        if self.range_type == 'geomspace':
            if self.start == 0:
                error_message = 'Geometric sequence cannot include zero'
                Logger().error(error_message)
                raise ValueError(error_message)
        if self.range_type == 'range':
            if self.start > self.stop:
                warn_message = 'NumberRange or one of its subclasses is empty cause np.arange does not deal with start greater than stop.'
                Logger().warn(warn_message)
        values = []
        if self.range_type == 'range':
            if not self.step:
                values = (np.arange)(self.start, self.stop, dtype=self.num_type, **self.range_params)
            else:
                values = (np.arange)(self.start, self.stop, self.step, dtype=self.num_type, **self.range_params)
        else:
            if self.range_type == 'linspace':
                if self.num:
                    values = (np.linspace)(self.start, self.stop, num=self.num, dtype=self.num_type, **self.range_params)
                else:
                    values = (np.linspace)(self.start, self.stop, dtype=self.num_type, **self.range_params)
            elif self.range_type == 'logspace':
                if self.num:
                    values = (np.logspace)(self.start, self.stop, num=self.num, dtype=self.num_type, **self.range_params)
                else:
                    values = (np.logspace)(self.start, self.stop, dtype=self.num_type, **self.range_params)
            else:
                if self.range_type == 'geomspace':
                    if self.num:
                        values = (np.geomspace)(self.start, self.stop, num=self.num, dtype=self.num_type, **self.range_params)
                    else:
                        values = (np.geomspace)(self.start, self.stop, dtype=self.num_type, **self.range_params)
                if self.num_type == np.int32:
                    self.values = list(set([int(i) for i in values]))
                elif self.num_type == np.float32:
                    self.values = list(set([float(i) for i in values]))

    @property
    def range_type(self):
        return self._range_type

    @range_type.setter
    def range_type(self, value):
        range_types = ['range', 'linspace', 'logspace', 'geomspace']
        if value in range_types:
            self._range_type = value
        else:
            raise ValueError('Subclass of NumberRange supports only ' + str(range_types) + ' as range_type, not ' + repr(value))


class IntegerRange(NumberRange):
    __doc__ = '\n         Class for easily creating a range of integer numbers to be tested in hyperparameter optimization.\n\n         Parameters\n         ----------\n         * \'start\' [number]:\n            The start value for generating the number interval.\n            The resulting interval includes the value, default is 0.\n\n         * \'stop\' [number]:\n            The stop value for generating the number interval.\n\n            - if range_type == "range":\n              the end value is not included in the interval (see documentation of numpy.arange).\n            - if range_type == "linspace"\n              the end value is included in the interval,\n              unless endpoint is set to False (see documentation of numpy.linspace).\n           - if range_type == "logspace"\n              the end value is included in the interval,\n              unless endpoint is set to False (see documentation of numpy.logspace).\n\n         * \'range_type\' [str]:\n            Which method to use for generating the number interval.\n            Possible options:\n\n            - "range": numpy.arange is used to generate a list of values separated by the same step width.\n            - "linspace": numpy.linspace is used to generate a certain number of values between start and stop.\n            - "logspace": numpy.logspace is used to generate a logarithmically distributed range of a certain length.\n\n         * \'step\' [number, default=None, optional]:\n           if range_type == \'range\', the spacing between values.\n\n         * \'num\' [int, default=None, optional]:\n           if range_type == \'linspace\' or range_type == \'logspace\', the number of samples to generate.\n\n         * \'kwargs\' [dict, optional]:\n           Further parameters that should be passed to the numpy function chosen with range_type.\n       '

    def __init__(self, start, stop, range_type='range', step=None, num=None, **kwargs):
        (super().__init__)(start, stop, range_type, step, num, (np.int32), **kwargs)


class FloatRange(NumberRange):
    __doc__ = '\n          Class for easily creating a range of integer numbers to be tested in hyperparameter optimization.\n\n          Parameters\n          ----------\n          * \'start\' [number]:\n             The start value for generating the number interval.\n             The resulting interval includes the value, default is 0.\n\n          * \'stop\' [number]:\n             The stop value for generating the number interval.\n\n             - if range_type == "range":\n               the end value is not included in the interval (see documentation of numpy.arange).\n             - if range_type == "linspace"\n               the end value is included in the interval,\n               unless endpoint is set to False (see documentation of numpy.linspace).\n            - if range_type == "logspace"\n               the end value is included in the interval,\n               unless endpoint is set to False (see documentation of numpy.logspace).\n\n          * \'range_type\' [str]:\n             Which method to use for generating the number interval.\n             Possible options:\n\n             - "range": numpy.arange is used to generate a list of values separated by the same step width.\n             - "linspace": numpy.linspace is used to generate a certain number of values between start and stop.\n             - "logspace": numpy.logspace is used to generate a logarithmically distributed range of a certain length.\n\n          * \'step\' [number, default=None, optional]:\n            if range_type == \'range\', the spacing between values.\n\n          * \'num\' [int, default=None, optional]:\n            if range_type == \'linspace\' or range_type == \'logspace\', the number of samples to generate.\n\n          * \'kwargs\' [dict, optional]:\n            Further parameters that should be passed to the numpy function chosen with range_type.\n        '

    def __init__(self, start, stop, range_type='range', step=None, num=None, **kwargs):
        (super().__init__)(start, stop, range_type, step, num, (np.float32), **kwargs)