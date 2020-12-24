# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/modules/core/actions/get_attribute.py
# Compiled at: 2016-11-13 21:51:24
# Size of source mod 2**32: 785 bytes
from dyson.errors import DysonError
from dyson.utils.module import DysonModule
from dyson.utils.selectors import translate_selector

class GetAttributeModule(DysonModule):

    def run(self, webdriver, params):
        """
        Get an attribute of an element
        :param webdriver:
        :param params:
        :return:
        """
        if 'of' in params:
            if 'attribute' in params:
                element = params['of']
                attribute = params['attribute']
                strategy, selector = translate_selector(element, webdriver)
                return strategy(selector).get_attribute(attribute)
            raise DysonError('Key "attribute" required')
        else:
            raise DysonError('Key "of" required')