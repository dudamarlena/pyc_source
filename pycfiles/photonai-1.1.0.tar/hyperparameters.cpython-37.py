# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/projects_nils/photon_core/photonai/optimization/hyperparameters.py
# Compiled at: 2019-11-21 09:20:09
# Size of source mod 2**32: 11370 bytes
import numpy as np, random
import photonai.photonlogger.logger as logger

class PhotonHyperparam(object):

    def __init__(self, value):
        self.value = value

    def get_random_value(self, definite_list: bool=True):
        if definite_list:
            return random.choice(self.values)
        msg = 'The PhotonHyperparam has no own random function.'
        logger.error(msg)
        raise ValueError(msg)


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

    def transform--- This code section failed: ---

 L. 124         0  LOAD_FAST                'self'
                2  LOAD_ATTR                range_type
                4  LOAD_STR                 'geomspace'
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    42  'to 42'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                start
               14  LOAD_CONST               0
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    42  'to 42'

 L. 125        20  LOAD_STR                 'Geometric sequence cannot include zero'
               22  STORE_FAST               'error_message'

 L. 126        24  LOAD_GLOBAL              logger
               26  LOAD_METHOD              error
               28  LOAD_FAST                'error_message'
               30  CALL_METHOD_1         1  '1 positional argument'
               32  POP_TOP          

 L. 127        34  LOAD_GLOBAL              ValueError
               36  LOAD_FAST                'error_message'
               38  CALL_FUNCTION_1       1  '1 positional argument'
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            18  '18'
             42_1  COME_FROM             8  '8'

 L. 128        42  LOAD_FAST                'self'
               44  LOAD_ATTR                range_type
               46  LOAD_STR                 'range'
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE    78  'to 78'
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                start
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                stop
               60  COMPARE_OP               >
               62  POP_JUMP_IF_FALSE    78  'to 78'

 L. 129        64  LOAD_STR                 'NumberRange or one of its subclasses is empty cause np.arange does not deal with start greater than stop.'
               66  STORE_FAST               'warn_message'

 L. 131        68  LOAD_GLOBAL              logger
               70  LOAD_METHOD              warn
               72  LOAD_FAST                'warn_message'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  POP_TOP          
             78_0  COME_FROM            62  '62'
             78_1  COME_FROM            50  '50'

 L. 133        78  BUILD_LIST_0          0 
               80  STORE_FAST               'values'

 L. 135        82  LOAD_FAST                'self'
               84  LOAD_ATTR                range_type
               86  LOAD_STR                 'range'
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   172  'to 172'

 L. 136        92  LOAD_FAST                'self'
               94  LOAD_ATTR                step
               96  POP_JUMP_IF_TRUE    132  'to 132'

 L. 137        98  LOAD_GLOBAL              np
              100  LOAD_ATTR                arange
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                start
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                stop
              110  BUILD_TUPLE_2         2 
              112  LOAD_STR                 'dtype'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                num_type
              118  BUILD_MAP_1           1 
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                range_params
              124  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              126  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              128  STORE_FAST               'values'
              130  JUMP_FORWARD        466  'to 466'
            132_0  COME_FROM            96  '96'

 L. 139       132  LOAD_GLOBAL              np
              134  LOAD_ATTR                arange
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                start
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                stop
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                step
              148  BUILD_TUPLE_3         3 
              150  LOAD_STR                 'dtype'
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                num_type
              156  BUILD_MAP_1           1 
              158  LOAD_FAST                'self'
              160  LOAD_ATTR                range_params
              162  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              164  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              166  STORE_FAST               'values'
          168_170  JUMP_FORWARD        466  'to 466'
            172_0  COME_FROM            90  '90'

 L. 140       172  LOAD_FAST                'self'
              174  LOAD_ATTR                range_type
              176  LOAD_STR                 'linspace'
              178  COMPARE_OP               ==
          180_182  POP_JUMP_IF_FALSE   262  'to 262'

 L. 141       184  LOAD_FAST                'self'
              186  LOAD_ATTR                num
              188  POP_JUMP_IF_FALSE   228  'to 228'

 L. 142       190  LOAD_GLOBAL              np
              192  LOAD_ATTR                linspace
              194  LOAD_FAST                'self'
              196  LOAD_ATTR                start
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                stop
              202  BUILD_TUPLE_2         2 
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                num
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                num_type
              212  LOAD_CONST               ('num', 'dtype')
              214  BUILD_CONST_KEY_MAP_2     2 
              216  LOAD_FAST                'self'
              218  LOAD_ATTR                range_params
              220  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              222  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              224  STORE_FAST               'values'
              226  JUMP_FORWARD        260  'to 260'
            228_0  COME_FROM           188  '188'

 L. 144       228  LOAD_GLOBAL              np
              230  LOAD_ATTR                linspace
              232  LOAD_FAST                'self'
              234  LOAD_ATTR                start
              236  LOAD_FAST                'self'
              238  LOAD_ATTR                stop
              240  BUILD_TUPLE_2         2 
              242  LOAD_STR                 'dtype'
              244  LOAD_FAST                'self'
              246  LOAD_ATTR                num_type
              248  BUILD_MAP_1           1 
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                range_params
              254  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              256  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              258  STORE_FAST               'values'
            260_0  COME_FROM           226  '226'
              260  JUMP_FORWARD        466  'to 466'
            262_0  COME_FROM           180  '180'

 L. 145       262  LOAD_FAST                'self'
              264  LOAD_ATTR                range_type
              266  LOAD_STR                 'logspace'
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   376  'to 376'

 L. 146       274  LOAD_FAST                'self'
              276  LOAD_ATTR                num_type
              278  LOAD_GLOBAL              np
              280  LOAD_ATTR                int32
              282  COMPARE_OP               ==
          284_286  POP_JUMP_IF_FALSE   296  'to 296'

 L. 147       288  LOAD_GLOBAL              ValueError
              290  LOAD_STR                 'Cannot use logspace for integer,  use geomspace instead.'
              292  CALL_FUNCTION_1       1  '1 positional argument'
              294  RAISE_VARARGS_1       1  'exception instance'
            296_0  COME_FROM           284  '284'

 L. 148       296  LOAD_FAST                'self'
              298  LOAD_ATTR                num
          300_302  POP_JUMP_IF_FALSE   342  'to 342'

 L. 149       304  LOAD_GLOBAL              np
              306  LOAD_ATTR                logspace
              308  LOAD_FAST                'self'
              310  LOAD_ATTR                start
              312  LOAD_FAST                'self'
              314  LOAD_ATTR                stop
              316  BUILD_TUPLE_2         2 
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                num
              322  LOAD_FAST                'self'
              324  LOAD_ATTR                num_type
              326  LOAD_CONST               ('num', 'dtype')
              328  BUILD_CONST_KEY_MAP_2     2 
              330  LOAD_FAST                'self'
              332  LOAD_ATTR                range_params
              334  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              336  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              338  STORE_FAST               'values'
              340  JUMP_FORWARD        374  'to 374'
            342_0  COME_FROM           300  '300'

 L. 151       342  LOAD_GLOBAL              np
              344  LOAD_ATTR                logspace
              346  LOAD_FAST                'self'
              348  LOAD_ATTR                start
              350  LOAD_FAST                'self'
              352  LOAD_ATTR                stop
              354  BUILD_TUPLE_2         2 
              356  LOAD_STR                 'dtype'
              358  LOAD_FAST                'self'
              360  LOAD_ATTR                num_type
              362  BUILD_MAP_1           1 
              364  LOAD_FAST                'self'
              366  LOAD_ATTR                range_params
              368  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              370  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              372  STORE_FAST               'values'
            374_0  COME_FROM           340  '340'
              374  JUMP_FORWARD        466  'to 466'
            376_0  COME_FROM           270  '270'

 L. 152       376  LOAD_FAST                'self'
              378  LOAD_ATTR                range_type
              380  LOAD_STR                 'geomspace'
              382  COMPARE_OP               ==
          384_386  POP_JUMP_IF_FALSE   466  'to 466'

 L. 153       388  LOAD_FAST                'self'
              390  LOAD_ATTR                num
          392_394  POP_JUMP_IF_FALSE   434  'to 434'

 L. 154       396  LOAD_GLOBAL              np
              398  LOAD_ATTR                geomspace
              400  LOAD_FAST                'self'
              402  LOAD_ATTR                start
              404  LOAD_FAST                'self'
              406  LOAD_ATTR                stop
              408  BUILD_TUPLE_2         2 
              410  LOAD_FAST                'self'
              412  LOAD_ATTR                num
              414  LOAD_FAST                'self'
              416  LOAD_ATTR                num_type
              418  LOAD_CONST               ('num', 'dtype')
              420  BUILD_CONST_KEY_MAP_2     2 
              422  LOAD_FAST                'self'
              424  LOAD_ATTR                range_params
            426_0  COME_FROM           130  '130'
              426  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              428  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              430  STORE_FAST               'values'
              432  JUMP_FORWARD        466  'to 466'
            434_0  COME_FROM           392  '392'

 L. 156       434  LOAD_GLOBAL              np
              436  LOAD_ATTR                geomspace
              438  LOAD_FAST                'self'
              440  LOAD_ATTR                start
              442  LOAD_FAST                'self'
              444  LOAD_ATTR                stop
              446  BUILD_TUPLE_2         2 
              448  LOAD_STR                 'dtype'
              450  LOAD_FAST                'self'
              452  LOAD_ATTR                num_type
              454  BUILD_MAP_1           1 
              456  LOAD_FAST                'self'
              458  LOAD_ATTR                range_params
              460  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              462  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              464  STORE_FAST               'values'
            466_0  COME_FROM           432  '432'
            466_1  COME_FROM           384  '384'
            466_2  COME_FROM           374  '374'
            466_3  COME_FROM           260  '260'
            466_4  COME_FROM           168  '168'

 L. 158       466  LOAD_FAST                'self'
              468  LOAD_ATTR                num_type
              470  LOAD_GLOBAL              np
              472  LOAD_ATTR                int32
              474  COMPARE_OP               ==
          476_478  POP_JUMP_IF_FALSE   498  'to 498'

 L. 159       480  LOAD_LISTCOMP            '<code_object <listcomp>>'
              482  LOAD_STR                 'NumberRange.transform.<locals>.<listcomp>'
              484  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              486  LOAD_FAST                'values'
              488  GET_ITER         
              490  CALL_FUNCTION_1       1  '1 positional argument'
              492  LOAD_FAST                'self'
              494  STORE_ATTR               values
              496  JUMP_FORWARD        528  'to 528'
            498_0  COME_FROM           476  '476'

 L. 160       498  LOAD_FAST                'self'
              500  LOAD_ATTR                num_type
              502  LOAD_GLOBAL              np
              504  LOAD_ATTR                float32
              506  COMPARE_OP               ==
          508_510  POP_JUMP_IF_FALSE   528  'to 528'

 L. 161       512  LOAD_LISTCOMP            '<code_object <listcomp>>'
              514  LOAD_STR                 'NumberRange.transform.<locals>.<listcomp>'
              516  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              518  LOAD_FAST                'values'
              520  GET_ITER         
              522  CALL_FUNCTION_1       1  '1 positional argument'
              524  LOAD_FAST                'self'
              526  STORE_ATTR               values
            528_0  COME_FROM           508  '508'
            528_1  COME_FROM           496  '496'

Parse error at or near `COME_FROM' instruction at offset 426_0

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

    def get_random_value(self, definite_list: bool=False):
        if definite_list:
            if not self.values:
                msg = 'No values were set. Please use transform method.'
                logger.error(msg)
                raise ValueError(msg)
            return random.choice(self.values)
        return random.randint(self.start, self.stop - 1)


class FloatRange(NumberRange):
    __doc__ = '\n          Class for easily creating a range of integer numbers to be tested in hyperparameter optimization.\n\n          Parameters\n          ----------\n          * \'start\' [number]:\n             The start value for generating the number interval.\n             The resulting interval includes the value, default is 0.\n\n          * \'stop\' [number]:\n             The stop value for generating the number interval.\n\n             - if range_type == "range":\n               the end value is not included in the interval (see documentation of numpy.arange).\n             - if range_type == "linspace"\n               the end value is included in the interval,\n               unless endpoint is set to False (see documentation of numpy.linspace).\n            - if range_type == "logspace"\n               the end value is included in the interval,\n               unless endpoint is set to False (see documentation of numpy.logspace).\n\n          * \'range_type\' [str]:\n             Which method to use for generating the number interval.\n             Possible options:\n\n             - "range": numpy.arange is used to generate a list of values separated by the same step width.\n             - "linspace": numpy.linspace is used to generate a certain number of values between start and stop.\n             - "logspace": numpy.logspace is used to generate a logarithmically distributed range of a certain length.\n\n          * \'step\' [number, default=None, optional]:\n            if range_type == \'range\', the spacing between values.\n\n          * \'num\' [int, default=None, optional]:\n            if range_type == \'linspace\' or range_type == \'logspace\', the number of samples to generate.\n\n          * \'kwargs\' [dict, optional]:\n            Further parameters that should be passed to the numpy function chosen with range_type.\n        '

    def __init__(self, start, stop, range_type='range', step=None, num=None, **kwargs):
        (super().__init__)(start, stop, range_type, step, num, (np.float32), **kwargs)

    def get_random_value(self, definite_list: bool=False):
        if definite_list:
            if not self.values:
                msg = 'No values were set. Please use transform method.'
                logger.error(msg)
                raise ValueError(msg)
            return random.choice(self.values)
        return random.uniform(self.start, self.stop)