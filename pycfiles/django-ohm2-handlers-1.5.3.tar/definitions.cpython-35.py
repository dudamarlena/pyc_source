# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/currencies/definitions.py
# Compiled at: 2016-12-06 14:21:50
# Size of source mod 2**32: 882 bytes
from ohm2_handlers.definitions import HandlersRunException, HandlersInputException, HandlersMethodException
from . import settings

class CurrenciesRunException(HandlersRunException):

    def __init__(self, *args, **kwargs):
        kwargs['app'] = 'currencies'
        kwargs['save'] = settings.SAVE_RUN_EXCEPTIONS
        super(CurrenciesRunException, self).__init__(*args, **kwargs)


class CurrenciesInputException(HandlersInputException):

    def __init__(self, *args, **kwargs):
        kwargs['app'] = 'currencies'
        kwargs['save'] = settings.SAVE_INPUT_EXCEPTIONS
        super(CurrenciesInputException, self).__init__(*args, **kwargs)


class CurrenciesMethodException(HandlersMethodException):

    def __init__(self, method, address, **kwargs):
        kwargs['app'] = 'currencies'
        kwargs['save'] = settings.SAVE_METHOD_EXCEPTIONS
        super(CurrenciesMethodException, self).__init__(method, address, **kwargs)