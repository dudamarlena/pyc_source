# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neo/validation.py
# Compiled at: 2014-01-17 10:34:23
from django.core.validators import RegexValidator, validate_email
from django.core.exceptions import ValidationError

def validate(fieldname, value):
    validator_name = 'validate_%s' % fieldname
    if validator_name in globals():
        globals()[validator_name](value)


validate_mobile_number = RegexValidator(regex='^[\\+]?[0-9]*$')
validate_login_alias = RegexValidator(regex='[^ +A-Z]{4,}')