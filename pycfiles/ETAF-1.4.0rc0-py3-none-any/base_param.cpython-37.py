# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/base_param.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 5886 bytes
import builtins, json, os
from federatedml.util import consts

class BaseParam(object):

    def __init__(self):
        pass

    def check(self):
        raise NotImplementedError('Parameter Object should have be check')

    def validate(self):
        self.builtin_types = dir(builtins)
        self.func = {'ge':self._greater_equal_than,  'le':self._less_equal_than, 
         'in':self._in, 
         'not_in':self._not_in, 
         'range':self._range}
        home_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        param_validation_path_prefix = home_dir + '/param_validation/'
        param_name = type(self).__name__
        param_validation_path = '/'.join([param_validation_path_prefix, param_name + '.json'])
        validation_json = None
        print('param validation path is {}'.format(home_dir))
        try:
            with open(param_validation_path, 'r') as (fin):
                validation_json = json.loads(fin.read())
        except:
            return
        else:
            self._validate_param(self, validation_json)

    def _validate_param(self, param_obj, validation_json):
        default_section = type(param_obj).__name__
        var_list = param_obj.__dict__
        for variable in var_list:
            attr = getattr(param_obj, variable)
            if type(attr).__name__ in self.builtin_types or attr is None:
                if variable not in validation_json:
                    continue
                validation_dict = validation_json[default_section][variable]
                value = getattr(param_obj, variable)
                value_legal = False
                for op_type in validation_dict:
                    if self.func[op_type](value, validation_dict[op_type]):
                        value_legal = True
                        break

                if not value_legal:
                    raise ValueError('Plase check runtime conf, {} = {} does not match user-parameter restriction'.format(variable, value))
                elif variable in validation_json:
                    self._validate_param(attr, validation_json)

    @staticmethod
    def check_string(param, descr):
        if type(param).__name__ not in ('str', ):
            raise ValueError(descr + ' {} not supported, should be string type'.format(param))

    @staticmethod
    def check_positive_integer(param, descr):
        if type(param).__name__ not in ('int', 'long') or param <= 0:
            raise ValueError(descr + ' {} not supported, should be positive integer'.format(param))

    @staticmethod
    def check_positive_number(param, descr):
        if type(param).__name__ not in ('float', 'int', 'long') or param <= 0:
            raise ValueError(descr + ' {} not supported, should be positive numeric'.format(param))

    @staticmethod
    def check_decimal_float(param, descr):
        if type(param).__name__ not in ('float', ) or param < 0 or param > 1:
            raise ValueError(descr + ' {} not supported, should be a float number in range [0, 1]'.format(param))

    @staticmethod
    def check_boolean(param, descr):
        if type(param).__name__ != 'bool':
            raise ValueError(descr + ' {} not supported, should be bool type'.format(param))

    @staticmethod
    def check_open_unit_interval(param, descr):
        if type(param).__name__ not in ('float', ) or param <= 0 or param >= 1:
            raise ValueError(descr + ' should be a numeric number between 0 and 1 exclusively')

    @staticmethod
    def check_valid_value(param, descr, valid_values):
        if param not in valid_values:
            raise ValueError(descr + ' {} is not supported, it should be in {}'.format(param, valid_values))

    @staticmethod
    def check_defined_type(param, descr, types):
        if type(param).__name__ not in types:
            raise ValueError(descr + ' {} not supported, should be one of {}'.format(param, types))

    @staticmethod
    def check_and_change_lower(param, valid_list, descr=''):
        if type(param).__name__ != 'str':
            raise ValueError(descr + ' {} not supported, should be one of {}'.format(param, valid_list))
        lower_param = param.lower()
        if lower_param in valid_list:
            return lower_param
        raise ValueError(descr + ' {} not supported, should be one of {}'.format(param, valid_list))

    @staticmethod
    def _greater_equal_than(value, limit):
        return value >= limit - consts.FLOAT_ZERO

    @staticmethod
    def _less_equal_than(value, limit):
        return value <= limit + consts.FLOAT_ZERO

    @staticmethod
    def _range(value, ranges):
        in_range = False
        for left_limit, right_limit in ranges:
            if left_limit - consts.FLOAT_ZERO <= value <= right_limit + consts.FLOAT_ZERO:
                in_range = True
                break

        return in_range

    @staticmethod
    def _in(value, right_value_list):
        return value in right_value_list

    @staticmethod
    def _not_in(value, wrong_value_list):
        return value not in wrong_value_list