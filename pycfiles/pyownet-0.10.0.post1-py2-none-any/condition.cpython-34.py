# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/alertapi30/condition.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 1868 bytes
from pyowm.utils import stringutils

class Condition:
    """Condition"""

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