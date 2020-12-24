# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/alertapi30/condition.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 1868 bytes
from pyowm.utils import stringutils

class Condition:
    __doc__ = '\n    Object representing a condition to be checked on a specific weather parameter. A condition is given when comparing\n    the weather parameter against a numerical value with respect to an operator.\n    Allowed weather params and operators are specified by the `pyowm.utils.alertapi30.WeatherParametersEnum` and\n    `pyowm.utils.alertapi30.OperatorsEnum` enumerator classes.\n    :param weather_param: the weather variable to be checked (eg. TEMPERATURE, CLOUDS, ...)\n    :type weather_param: str\n    :param operator: the comparison operator to be applied to the weather variable (eg. GREATER_THAN, EQUAL, ...)\n    :type operator: str\n    :param amount: comparison value\n    :type amount: int or float\n    :param id: optional unique ID for this Condition instance\n    :type id: str\n    :returns:  a *Condition* instance\n    :raises: *AssertionError* when either the weather param has wrong type or the operator has wrong type or the\n    amount has wrong type\n\n    '

    def __init__(self, weather_param, operator, amount, id=None):
        assert weather_param is not None
        assert isinstance(weather_param, str), 'Value must be a string'
        self.weather_param = weather_param
        assert operator is not None
        assert isinstance(operator, str), 'Value must be a string'
        self.operator = operator
        assert amount is not None
        if not isinstance(amount, int):
            assert isinstance(amount, float)
        self.amount = amount
        self.id = id

    @classmethod
    def from_dict(cls, the_dict):
        assert isinstance(the_dict, dict)
        weather_param = the_dict['name']
        operator = the_dict['expression']
        amount = the_dict['amount']
        the_id = the_dict.get('_id', None)
        return Condition(weather_param, operator, amount, id=the_id)