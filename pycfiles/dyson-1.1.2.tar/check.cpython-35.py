# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/modules/core/actions/check.py
# Compiled at: 2016-11-11 04:04:15
# Size of source mod 2**32: 875 bytes
from dyson.errors import DysonError
from dyson.utils.module import DysonModule
from dyson.utils.selectors import translate_selector

class CheckModule(DysonModule):

    def run(self, webdriver, params):
        """
        Check an element on the page.
        Usually only applies to radio and
        checkbox's
        :param webdriver:
        :param params:
        :return:
        """
        if len(params.keys()) > 0:
            selector, strategy = translate_selector(params, webdriver)
            if selector and strategy:
                element = selector(strategy)
                if not element.is_selected():
                    return selector(strategy).click()
            else:
                raise DysonError('You need to specify a valid selector to check')
        else:
            raise DysonError('You need to specify an argument to "check"')