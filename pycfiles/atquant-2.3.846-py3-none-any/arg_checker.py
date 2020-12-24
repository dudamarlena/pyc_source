# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\utils\arg_checker.py
# Compiled at: 2018-08-27 20:45:27
# Size of source mod 2**32: 15626 bytes
import datetime, inspect, traceback, types
from functools import lru_cache
from functools import wraps
import numpy as np, pandas as pd
from dateutil.parser import parse as parse_date
from atquant.data.const_data import atGetAllPriceType
from atquant.utils.datetime_func import to_datetime
from atquant.utils.internal_util import unwrapper
from atquant.utils.logger import write_userlog, LoggerManager

class ATInvalidArgument(Exception):
    pass


class ArgumnetChecker:
    __doc__ = "\n    执行参数检查，使用方法如下:\n    \n    @apply_rule(verify_that('KFrequency').is_valid_frequency(),\n            verify_that('DateSpan').is_greater_or_equal_than(0),\n            verify_that('FillUp').is_instance_of(bool))\n    def traderAppendKDataScope(KFrequency, DateSpan, FillUp):\n        pass\n    "
    PRICE_TYPE = [
     'market', 'limit']
    FREQUENCY = ['day', 'min', 'sec', 'tick', 'week', 'month']
    STOP_TYPE = ['point', 'percent']
    TRAILING_TYPE = ['point', 'percent']
    ORDER_CTG = ['market', 'limit']

    def __init__(self, arg_name):
        self._arg_name = arg_name
        self._rules = []

    def is_instance_of(self, types):

        def _is_instance_of(func_name, value):
            return self._is_instance_of(types, func_name, value)

        self._rules.append(_is_instance_of)
        return self

    def _is_instance_of(self, types, func_name, value):
        if not isinstance(value, types):
            raise ATInvalidArgument('function {}: invalid {} argument, except a value of type {}, got {} (type: {})'.format(func_name, self._arg_name, types, value, type(value)))
        return self

    def is_empty_or_not(self, empty=False, ignore_none=True):

        def empty_or_not(func_name, value):
            if ignore_none and value is None:
                return
            if empty and len(value) > 0:
                raise ATInvalidArgument('function {}: invalid {} argument, except len = 0, got {} (type: {})'.format(func_name, self._arg_name, value, type(value)))
            if not empty and len(value) < 1:
                raise ATInvalidArgument('function {}: invalid {} argument, except len > 0, got {} (type: {})'.format(func_name, self._arg_name, value, type(value)))

        self._rules.append(empty_or_not)
        return self

    def _is_in(self, func_name, value, valid_values, ignore_value=True):
        if ignore_value and value is None:
            return
        if value not in valid_values:
            raise ATInvalidArgument('function {}: invalid {} argument, valid: {}, got {} (type: {})'.format(func_name, self._arg_name, repr(valid_values), value, type(value)))

    def is_in(self, valid_values, ignore_value=True):

        def check_is_in(func_name, value):
            return self._is_in(func_name, value, valid_values, ignore_value)

        self._rules.append(check_is_in)
        return self

    def is_price_type(self):

        def check_price_type(func_name, value):
            if value not in self.PRICE_TYPE:
                raise ATInvalidArgument('function {}: invalid {} argument, valid: {}, got {} (type: {})'.format(func_name, self._arg_name, repr(self.PRICE_TYPE), value, type(value)))

        self._rules.append(check_price_type)
        return self

    def is_stop_type(self):

        def check_stop_type(func_name, value):
            if not isinstance(value, str) or value.lower() not in self.STOP_TYPE:
                raise ATInvalidArgument('function {}: invalid {} argument, valid: {}, got {} (type: {})'.format(func_name, self._arg_name, repr(self.STOP_TYPE), value, type(value)))

        self._rules.append(check_stop_type)
        return self

    def is_callable(self):

        def check_callable_type(func_name, value):
            if callable(value) is False:
                raise ATInvalidArgument('function {}: invalid {} argument, expect function type, got {} (type: {})'.format(func_name, self._arg_name, value, type(value)))

        self._rules.append(check_callable_type)
        return self

    def is_trailing_type(self):

        def check_trailing_type(func_name, value):
            if not isinstance(value, str) or value.lower() not in self.TRAILING_TYPE:
                raise ATInvalidArgument('function {}: invalid {} argument, valid: {}, got {} (type: {})'.format(func_name, self._arg_name, repr(self.TRAILING_TYPE), value, type(value)))

        self._rules.append(check_trailing_type)
        return self

    def is_oder_ctg(self):

        def check_oder_ctg(func_name, value):
            if not isinstance(value, str) or value.lower() not in self.ORDER_CTG:
                raise ATInvalidArgument('function {}: invalid {} argument, valid: {}, got {} (type: {})'.format(func_name, self._arg_name, repr(self.ORDER_CTG), value, type(value)))

        self._rules.append(check_oder_ctg)
        return self

    def is_valid_date(self, timestamp=False):

        def check_is_valid_date(func_name, value):
            if isinstance(value, (datetime.date, pd.Timestamp)):
                return
            if isinstance(value, (int, str)):
                if value == 0:
                    return
                try:
                    if not timestamp:
                        datetime.datetime.strptime(str(value), '%Y%m%d')
                    else:
                        parse_date(value)
                except Exception:
                    raise ATInvalidArgument('function {}: invalid {} argument, except a valid date, got {} (type: {})'.format(func_name, self._arg_name, value, type(value)))

        self._rules.append(check_is_valid_date)
        return self

    def is_future_date(self):

        def check_future_date(func_name, value):
            try:
                if not isinstance(value, (int, str)):
                    raise ATInvalidArgument('function {}: invalid {} argument, except type int, got {} (type: {})'.format(func_name, self._arg_name, value, type(value)))
                if value == 0:
                    return
                dt = datetime.datetime.strptime(str(value), '%Y%m%d')
                if dt > datetime.datetime.now():
                    raise ATInvalidArgument('Date %s is funture date' % value)
            except ValueError:
                raise ATInvalidArgument('function {}: invalid {} argument, except a valid date,like:20180303, got {} (type: {})'.format(func_name, self._arg_name, value, type(value)))

        self._rules.append(check_future_date)
        return self

    def is_greater_than(self, low):

        def check_greater_than(func_name, value):
            if value <= low:
                raise ATInvalidArgument('function {}: invalid {} argument, except a value > {}, got {} (type: {})'.format(func_name, self._arg_name, low, value, type(value)))

        self._rules.append(check_greater_than)
        return self

    def _is_greater_or_equal_than(self, low, func_name, value):
        if value < low:
            raise ATInvalidArgument('function {}: invalid {} argument, except a value >= {}, got {} (type: {})'.format(func_name, self._arg_name, low, value, type(value)))
        return self

    def is_greater_or_equal_than(self, low):

        def check_greater_or_equal_than(func_name, value):
            return self._is_greater_or_equal_than(low, func_name, value)

        self._rules.append(check_greater_or_equal_than)
        return self

    def is_less_than(self, high):

        def check_less_than(func_name, value):
            if value >= high:
                raise ATInvalidArgument('function {}: invalid {} argument, except a value < {}, got {} (type: {})'.format(func_name, self._arg_name, high, value, type(value)))

        self._rules.append(check_less_than)
        return self

    def is_less_or_equal_than(self, high):

        def check_less_or_equal_than(func_name, value):
            if value >= high:
                raise ATInvalidArgument('function {}: invalid {} argument, except a value >= {}, got {} (type: {})'.format(func_name, self._arg_name, high, value, type(value)))

        self._rules.append(check_less_or_equal_than)
        return self

    def _is_valid_frequency(self, func_name, value):
        valid = isinstance(value, str) and value in self.FREQUENCY
        if not valid:
            raise ATInvalidArgument('function {}: invalid {} argument, frequency should be in form of "day","min","sec","tick", got {} (type: {})'.format(func_name, self.arg_name, value, type(value)))

    def is_valid_frequency(self):
        self._rules.append(self._is_valid_frequency)
        return self

    def _is_valid_fq(self, func_name, value):
        valid = isinstance(value, str) and value in ('NA', 'FWard', 'BWard')
        if not valid:
            raise ATInvalidArgument('function {}: invalid {} argument, FQ should be in form of "NA","FWard","BWard", got {} (type: {})'.format(func_name, self.arg_name, value, type(value)))

    def is_valid_fq(self):
        self._rules.append(self._is_valid_fq)
        return self

    def is_valid_price_type(self):

        def check_validate_orderctg(func_name, value):
            alltype = atGetAllPriceType()
            ss = '[%s]' % ','.join(alltype)
            if value.upper() not in alltype:
                raise ATInvalidArgument('function {}: invalid {} argument, except one of {}, got {} (type: {})'.format(func_name, self._arg_name, ss, value, type(value)))

        self._rules.append(self.check_validate_orderctg)
        return self

    def is_valid_order_act(self):

        def check_validate_orderact(func_name, value):
            acts = [
             'sell', 'buy']
            ss = '[%s]' % ','.join(acts)
            if value.upper() not in acts:
                raise ATInvalidArgument('function {}: invalid {} argument, except one of {}, got {} (type: {})'.format(func_name, self._arg_name, ss, value, type(value)))

        self._rules.append(self.check_validate_orderctg)
        return self

    def verify(self, func_name, value):
        for r in self._rules:
            r(func_name, value)

    @property
    def arg_name(self):
        return self._arg_name

    @classmethod
    @lru_cache(None)
    def check_begindate_enddate(cls, begin, end):
        """
        一、输入的整形数据是否符合datatime的要求
        二、判断输入的时间是否在可控区间内
        三、结束时间不能小于开始时间
        :param begin: int/str, like: 20120119
        :param end: int/str, like:20120120
        :return: None
        """
        _b = to_datetime(begin)
        _e = to_datetime(end)
        MIN_TIME = datetime(1900, 1, 1)
        NOW_TIME = datetime.now()
        if MIN_TIME < _b < NOW_TIME:
            if MIN_TIME < _e < NOW_TIME:
                if _b > _b:
                    raise ValueError('start date {} > stop date {}'.format(_b, _e))
        else:
            raise ValueError('Expect date from 1900 to now')

    @classmethod
    def is_algorithm_func_and_args(cls, func_name, *args):
        if len(args) > 2:
            raise ATInvalidArgument('function {}: invalid argument, except 2 args, got {} (type: {})'.format(func_name, repr(*args), type(*args)))
        if len(args) == 0:
            return
        if len(args) == 1:
            if not isinstance(args[0], types.FunctionType):
                raise ATInvalidArgument('function {}: invalid argument, except FunctionType, got {} (type: {})'.format(func_name, args[0], type(args[0])))

    @staticmethod
    def check_ndarray_idx(func_name, parame_name, value, dtype=np.int, allow_none=False, allow_nan=False):
        """value 必须是一个 tuple/list, 包含 idx(np.ndarray), idx 最小值(闭区间), idx 最大值(开区间)"""
        nd, minvalue, maxvalue = value[0], value[1], value[2]
        if isinstance(nd, np.ndarray):
            nd = nd.ravel()
            if nd.size < 1:
                raise ATInvalidArgument('function {}: invalid {} argument, except at least 1 value, got 0 size'.format(func_name, parame_name))
            if dtype is not None and nd.dtype != dtype:
                raise ATInvalidArgument('function {}: invalid {} argument, except dtype {} , got dtype {}'.format(func_name, parame_name, str(dtype), str(nd.dtype)))
            if not allow_none:
                none_type = type(None)
                for item in nd:
                    if type(item) == none_type:
                        raise ATInvalidArgument('function {}: invalid {} argument, value items unexcept contains None value'.format(func_name, parame_name))

            if not allow_nan:
                if np.any(np.isnan(nd)):
                    raise ATInvalidArgument('function {}: invalid {} argument, value items unexcept contains NaN value'.format(func_name, parame_name))
            if minvalue is not None and np.min(nd) < minvalue:
                raise ATInvalidArgument('function {}: invalid {} argument, error value items index < {}'.format(func_name, parame_name, minvalue))
            if maxvalue is not None and np.max(nd) >= maxvalue:
                raise ATInvalidArgument('function {}: invalid {} argument, error value items index > {}'.format(func_name, parame_name, maxvalue))
        else:
            raise ATInvalidArgument('function {}: invalid {} argument, except numpy.ndarry type,got {} type'.format(func_name, parame_name, type(nd)))


def verify_that(arg_name):
    return ArgumnetChecker(arg_name)


def apply_rule(*rules):

    def decorator(func):

        @wraps(func)
        def api_rule_check_wrapper(*args, **kwargs):
            try:
                call_args = inspect.getcallargs(unwrapper(func), *args, **kwargs)
                for r in rules:
                    r.verify(func.__name__, call_args[r.arg_name])

                return func(*args, **kwargs)
            except ATInvalidArgument as e:
                print(e, ', see detail log "%s" ' % LoggerManager.user_logpath())
                write_userlog(traceback.format_exc(), 'error')
                exit(-1)
            except Exception as e:
                print(e, ', see detail log "%s" ' % LoggerManager.user_logpath())
                write_userlog(traceback.format_exc(), 'error')
                exit(-1)

        return api_rule_check_wrapper

    return decorator