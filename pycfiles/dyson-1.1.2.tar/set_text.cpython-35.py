# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/modules/core/actions/set_text.py
# Compiled at: 2016-11-11 04:04:52
# Size of source mod 2**32: 607 bytes
from dyson.errors import DysonError
from dyson.utils.module import DysonModule
from dyson.utils.selectors import translate_selector

class SetTextModule(DysonModule):

    def run(self, webdriver, params):
        """
        Set the text of an input
        :param webdriver:
        :param params:
        :return:
        """
        if 'of' in params and 'to' in params:
            strategy, selector = translate_selector(params['of'], webdriver=webdriver)
            return strategy(selector).send_keys(params['to'])
        raise DysonError('Keys "of" and "to" are required')