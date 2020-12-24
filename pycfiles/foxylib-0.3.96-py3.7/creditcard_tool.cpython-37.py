# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/finance/creditcard/creditcard_tool.py
# Compiled at: 2020-01-15 23:57:40
# Size of source mod 2**32: 1764 bytes
import re
from functools import lru_cache
from foxylib.tools.function.function_tool import FunctionTool

class CreditcardCompany:

    class Value:
        VISA = 'visa'
        MASTERCARD = 'mastercard'
        DISCOVER = 'discover'
        AMEX = 'amex'
        DINERSCLUB = 'dinersclub'
        ETC = 'etc'

    V = Value

    @classmethod
    def rstr_visa(cls):
        return '4[0-9]{12}(?:[0-9]{3})?'

    @classmethod
    def rstr_mastercard(cls):
        return '(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}'

    @classmethod
    def rstr_amex(cls):
        return '3[47][0-9]{13}'

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_amex(cls):
        return re.compile(cls.rstr_amex())

    @classmethod
    def rstr_dinersclub(cls):
        return '3(?:0[0-5]|[68][0-9])[0-9]{11}'

    @classmethod
    def rstr_discover(cls):
        return '6(?:011|5[0-9]{2})[0-9]{12}'

    @classmethod
    def rstr_jcb(cls):
        return '(?:2131|1800|35\\d{3})\\d{11}'


class CreditcardTool:

    @classmethod
    def cardnumber2cvc_digit(cls, cardnumber):
        if CreditcardCompany.pattern_amex().match(cardnumber):
            return 4
        return 3