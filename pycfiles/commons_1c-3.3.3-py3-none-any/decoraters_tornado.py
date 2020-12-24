# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/commonslib/decoraters_tornado.py
# Compiled at: 2015-04-04 05:19:06
import copy, functools
from app.commons.validators import Validators
from app.commons.view_model import ViewModel
__author__ = 'freeway'

def validators(rules=None, messages=None):
    u"""validators decorater
    just for tornado
    会给self.对象加入
    :param rules: 校验规则
    :param messages: 出错信息

    """

    def _validators(method):

        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if rules is None or len(rules) == 0:
                return method(self, *args, **kwargs)
            else:
                validate = Validators()
                validate.rules = copy.deepcopy(rules)
                if messages is not None:
                    validate.messages = messages
                valid_data = ViewModel()
                for field_name, validator in validate.rules.iteritems():
                    valid_data[field_name] = self.get_argument(field_name, '')
                    for validate_type, validate_value in validator.iteritems():
                        if isinstance(validate_value, str) or isinstance(validate_value, unicode):
                            if '#' == validate_value[:1]:
                                validator[validate_type] = self.get_argument(validate_value[1:], '')

                self.validation_success = validate.validates(valid_data)
                self.validation_errors = validate.errors
                self.validation_data = valid_data
                return method(self, *args, **kwargs)

        return wrapper

    return _validators