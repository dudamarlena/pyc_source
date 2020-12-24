# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/validatish/util.py
# Compiled at: 2009-01-22 09:32:47
"""
Module of validatish utils.
"""
from validatish.validator import All, Any

def any(iterable):
    return False in (not x for x in iterable)


def all(iterable):
    return True not in (not x for x in iterable)


def validation_includes(validator, validator_type):
    """
    Test if the validator type exists in the validator graph.
    """
    if validator is None:
        return False
    else:
        if isinstance(validator, validator_type):
            return True
        if isinstance(validator, All):
            return any(validation_includes(v, validator_type) for v in validator.validators)
        if isinstance(validator, Any):
            included = any(validation_includes(v, validator_type) for v in validator.validators)
            same_type = all(isinstance(v, validator_type) for v in validator.validators)
            return included and same_type
        return False