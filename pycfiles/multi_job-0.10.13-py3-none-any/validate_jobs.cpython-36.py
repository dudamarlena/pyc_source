# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/multi-job/multi_job/validation/validate_jobs.py
# Compiled at: 2020-02-19 07:55:17
# Size of source mod 2**32: 1450 bytes
from .validation_utils import Result, Validator

def check_job_has_callable(config: dict) -> Result:
    return Result(True)


def check_job_callable_str(config: dict) -> Result:
    return Result(True)


def check_job_callable_exists(config: dict) -> Result:
    return Result(True)


def check_job_has_targets_xor_skips(config: dict) -> Result:
    return Result(True)


def check_job_targets_lst(config: dict) -> Result:
    return Result(True)


def check_job_valid_targets(config: dict) -> Result:
    return Result(True)


job_validators = [
 Validator('Job configuration', "Jobs must have a 'callable' ie a command xor script xor a function field", check_job_has_callable),
 Validator('Job configuration', "A job's callable field must be a string", check_job_callable_str),
 Validator('Job configuration', "A job's callable field must be resolvable", check_job_callable_exists),
 Validator('Job configuration', 'Jobs may only have a targets xor a skips field', check_job_has_targets_xor_skips),
 Validator('Job configuration', "A job's targets or skips field must be a list or 'all", check_job_targets_lst),
 Validator('Job configuration', "A job's targets or skips field must contain project names or 'all'", check_job_valid_targets)]