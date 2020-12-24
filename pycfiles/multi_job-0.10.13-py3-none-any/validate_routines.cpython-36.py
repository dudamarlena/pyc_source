# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/multi-job/multi_job/validation/validate_routines.py
# Compiled at: 2020-02-19 08:05:19
# Size of source mod 2**32: 473 bytes
from .validation_utils import Result, Validator

def check_routine_lst(config: dict) -> Result:
    return Result(True)


def check_routine_valid(config: dict) -> Result:
    return Result(True)


routine_validators = [
 Validator('Routine configuration', "Routines must be a list or 'all'", check_routine_lst),
 Validator('Routine configuration', "Routines may only contain job names or 'all'", check_routine_valid)]