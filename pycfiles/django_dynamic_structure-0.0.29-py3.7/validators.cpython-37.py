# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dyn_struct/db/validators.py
# Compiled at: 2016-09-04 10:55:37
# Size of source mod 2**32: 787 bytes
import json
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text

@deconstructible
class ParamsValidator(object):
    json_valid_error_message = 'Введите корректные JSON данные.'
    dict_valid_error_message = 'Данные должны иметь вид {"ключ": значение}.'
    code = 'invalid'

    def __call__(self, value):
        value = force_text(value)
        try:
            dict(json.loads(value))
        except json.JSONDecodeError:
            raise ValidationError((self.json_valid_error_message), code=(self.code))
        except TypeError:
            raise ValidationError((self.dict_valid_error_message), code=(self.code))