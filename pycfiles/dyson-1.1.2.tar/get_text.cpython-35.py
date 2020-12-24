# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/modules/core/actions/get_text.py
# Compiled at: 2016-11-15 01:57:10
# Size of source mod 2**32: 574 bytes
from dyson.errors import DysonError
from dyson.utils.module import DysonModule
from dyson.utils.selectors import translate_selector

class GetTextModule(DysonModule):

    def run(self, webdriver, params):
        """
        Get the text of a specific element (return innerText)
        :param webdriver:
        :param params:
        :return:
        """
        if 'of' in params:
            strategy, selector = translate_selector(params['of'], webdriver)
            return strategy(selector).text
        raise DysonError('Key "of" is required')